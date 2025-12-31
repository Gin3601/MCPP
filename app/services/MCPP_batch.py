from concurrent.futures import ThreadPoolExecutor, as_completed

from app.config import settings
from app.services.all_promot import get_prompt
from app.utils.http import post_edit, wait_for_outputs
from app.utils.logger import get_logger

logger = get_logger("MCPP_batch")


class ServiceError(Exception):
    pass


TASKS = ["main", "bigplate", "smallplate", "ground", "information"]


def _build_payload(task_name: str, images: dict, resolution: str = "1k") -> dict:
    # 统一把 edit_image 放到 images[0]，参考图排后面（符合你贴的 OpenAPI）
    for k in ("edit_image", "ref1", "ref2", "ref3"):
        if k not in images or not isinstance(images[k], str) or not images[k].strip():
            raise ServiceError(f"缺少图片URL: {k}")

    image_urls = [
        images["edit_image"].strip(),
        images["ref1"].strip(),
        images["ref2"].strip(),
        images["ref3"].strip(),
    ]

    return {
        "prompt": get_prompt(task_name),
        "images": image_urls,
        "enable_sync_mode": True,      # 同步优先
        "enable_base64_output": False,
        "resolution": resolution,      # 1k / 2k / 4k
    }


def run(task_name: str, images: dict, resolution: str) -> dict:
    payload = _build_payload(task_name, images, resolution=resolution)

    result = post_edit(
        api_url=settings.API_URL,
        api_key=settings.API_KEY,
        payload=payload,
    )

    data = result.get("data") if isinstance(result, dict) else None
    if not isinstance(data, dict):
        raise ServiceError(f"{task_name}: 上游返回格式异常: {result}")

    outputs = data.get("outputs") or []
    if outputs:
        return {"task": task_name, "output": outputs[0], "mode": "sync"}

    # 同步没拿到 outputs：异步兜底（不重复 POST，避免重复计费）
    result_url = (data.get("urls") or {}).get("get")
    if not result_url:
        raise ServiceError(f"{task_name}: 模型未返回 outputs 且缺少 urls.get: {result}")

    final = wait_for_outputs(result_url=result_url, api_key=settings.API_KEY, timeout_seconds=180, poll_interval=1.0)
    fdata = final.get("data") if isinstance(final, dict) else None
    foutputs = (fdata or {}).get("outputs") or []
    if not foutputs:
        raise ServiceError(f"{task_name}: 轮询后仍无 outputs: {final}")

    return {"task": task_name, "output": foutputs[0], "mode": "async"}


def run_all(images: dict, resolution: str = "1k", parallel: bool = True) -> dict:
    """
    一次性生成所有任务的输出。
    - parallel=True：并行请求（更快，但瞬时并发更高，可能遇到限流）
    - parallel=False：串行（更稳）
    """
    logger.info("MCPP_batch start, parallel=%s, resolution=%s", parallel, resolution)

    results: dict = {}
    errors: dict = {}

    if parallel:
        # 线程并行（requests 是阻塞的，适合用线程）
        with ThreadPoolExecutor(max_workers=min(5, len(TASKS))) as ex:
            futs = {ex.submit(run, t, images, resolution): t for t in TASKS}
            for fut in as_completed(futs):
                t = futs[fut]
                try:
                    r = fut.result()
                    results[t] = r
                except Exception as e:
                    logger.exception("MCPP_batch task failed: %s", t)
                    errors[t] = str(e)
    else:
        for t in TASKS:
            try:
                results[t] = run(t, images, resolution)         
            except Exception as e:
                logger.exception("MCPP_batch task failed: %s", t)
                errors[t] = str(e)

    ok = len(results) > 0 and len(errors) == 0
    logger.info("MCPP_batch done, ok=%s, results=%d, errors=%d", ok, len(results), len(errors))

    return {
        "status": "success" if ok else "partial" if results else "failed",
        "results": results,   # 每个 task 的 output url
        "errors": errors,     # 失败原因（如果有）
    }
