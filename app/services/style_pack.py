from typing import Any, Dict, List, Callable, Optional

from app.services.MCPP_main import run as main_run
from app.services.MCPP_ground import run as ground_run
from app.services.MCPP_ground2 import run as ground2_run
from app.services.MCPP_batch import run as batch_run
from app.services.MCPP_smallplate import run as smallplate_run
from app.services.MCPP_bigplate import run as bigplate_run

RUNNERS: Dict[str, Callable[..., Any]] = {
    "main": main_run,
    "ground": ground_run,
    "ground2": ground2_run,
    "smallplate": smallplate_run,
    "bigplate": bigplate_run,
    "batch": batch_run,
}

ALLOWED_TASKS = set(RUNNERS.keys())


def build_payload(task: str, urls: Dict[str, str]) -> Dict[str, Any]:
    """
    按任务名生成传给对应 service.run 的 images 参数（全部是 URL）
    你要换“不同风格”的逻辑，就改这里即可。
    """
    t = (task or "").lower()

    if t == "main":
        return {"edit_image": urls["edit"], "ref1": urls["ref1"]}

    if t == "ground":
        return {"edit_image": urls["edit"], "ref1": urls["ref2"]}

    if t == "ground2":
        return {"edit_image": urls["edit"], "ref1": urls["ref3"]}

    if t == "smallplate":
        return {"edit_image": urls["edit"], "ref1": urls["ref2"]}

    if t == "bigplate":
        return {"edit_image": urls["edit"], "ref1": urls["ref3"]}

    if t == "batch":
        # ⚠️ 这里按“batch_run 支持 images list”的写法示例
        # 如果你的 batch_run 不是这种结构，把 MCPP_batch.py 的 payload 那段贴我，我帮你改成完全一致
        return {"images": [urls["edit"], urls["ref1"], urls["ref2"]]}

    raise KeyError(f"Unknown task: {task}")


async def run_style_pack(
    urls: Dict[str, str],
    tasks: List[str],
    request: Any = None,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    只执行 tasks 指定的任务，避免多余 API 调用（省钱）。
    每个任务独立 try/except：一个失败不影响其他任务。
    """
    results: Dict[str, Any] = {}

    for task in tasks:
        t = (task or "").lower()

        if t not in RUNNERS:
            results[t] = {"status": "failed", "error": f"unknown task: {task}"}
            continue

        runner = RUNNERS[t]

        try:
            images_payload = build_payload(t, urls)
            r = await runner(images_payload, request=request, base_url=base_url)

            # 统一一下输出结构（不强制，主要方便前端稳定解析）
            if isinstance(r, dict):
                results[t] = {"status": r.get("status", "success"), **r}
            else:
                results[t] = {"status": "success", "result": r}

        except Exception as e:
            # ✅ 不让异常把整包带崩
            results[t] = {"status": "failed", "error": str(e)}

    return results
