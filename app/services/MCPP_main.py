from app.utils.http import post_edit, wait_for_outputs
from app.services.all_promot import get_prompt
from app.utils.logger import get_logger
from app.config import settings

logger = get_logger("MCPP_main")


class ServiceError(Exception):
    pass


def _normalize_images(images) -> list[str]:
    """
    允许你从接口层传：
    - list[str]：直接当作 images
    - dict：尝试从常见 key 中抽取 URL（edit_image/ref1/ref2/ref3）
    """
    if isinstance(images, list):
        urls = [x for x in images if isinstance(x, str) and x.strip()]
        return urls

    if isinstance(images, dict):
        # 兼容你现在的结构：{"edit_image": "...", "ref1": "...", ...}
        keys = ["edit_image", "ref1", "ref2", "ref3"]
        urls = []
        for k in keys:
            v = images.get(k)
            if isinstance(v, str) and v.strip():
                urls.append(v.strip())
        # 也允许 dict 里直接有 "images": [...]
        if not urls and isinstance(images.get("images"), list):
            urls = [x for x in images["images"] if isinstance(x, str) and x.strip()]
        return urls

    return []


def run(images):
    logger.info("MCPP_main start")

    try:
        image_urls = _normalize_images(images)
        if not image_urls:
            raise ServiceError("缺少图片URL：images 必须是 URL 列表，或包含 edit_image/ref1/ref2/ref3 的 dict")

        payload = {
            "prompt": get_prompt("main"),
            "images": image_urls,              # ✅ 必须是 array[string]
            "enable_sync_mode": True,          # ✅ 显式开启同步
            "enable_base64_output": False,
            "resolution": "1k",                # ✅ 可选：1k/2k/4k（按次收费）
            # "aspect_ratio": "4:3",           # 可选
            # 同步模式下不要传 callback
        }

        result = post_edit(
            api_url=settings.API_URL,
            api_key=settings.API_KEY,
            payload=payload,
        )

        data = result.get("data") if isinstance(result, dict) else None
        if not isinstance(data, dict):
            logger.error("MCPP_main invalid response: %s", result)
            raise ServiceError("上游返回格式异常")

        status = (data.get("status") or "").lower()
        outputs = data.get("outputs") or []

        # ✅ 同步成功：直接有 outputs
        if outputs:
            logger.info("MCPP_main success (sync)")
            return {"status": "success", "output": outputs[0], "mode": "sync"}

        # ✅ 同步没拿到结果：异步兜底（避免你现在的 400）
        result_url = (data.get("urls") or {}).get("get")
        if not result_url:
            logger.error("MCPP_main no outputs and no result url: %s", result)
            raise ServiceError("模型未返回结果且缺少结果查询地址")

        # 兜底等待一段时间（你可以调短/调长）
        final = wait_for_outputs(
            result_url=result_url,
            api_key=settings.API_KEY,
            timeout_seconds=180,
            poll_interval=1.0,
        )
        fdata = final.get("data") if isinstance(final, dict) else None
        foutputs = (fdata or {}).get("outputs") or []
        if not foutputs:
            logger.error("MCPP_main async done but still no outputs: %s", final)
            raise ServiceError("模型未返回结果")

        logger.info("MCPP_main success (async fallback)")
        return {"status": "success", "output": foutputs[0], "mode": "async"}

    except ServiceError:
        raise
    except Exception:
        logger.exception("MCPP_main crashed")
        raise ServiceError("MCPP_main internal error")
