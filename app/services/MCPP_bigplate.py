from app.utils.http import post_edit, wait_for_outputs
from app.config import settings
from app.services.all_promot import get_prompt
from app.utils.logger import get_logger

logger = get_logger("MCPP_bigplate")


class ServiceError(Exception):
    pass


def run(images: dict):
    logger.info("MCPP_bigplate start")

    try:
        # 基本校验
        for k in ("edit_image", "ref1", "ref2", "ref3"):
            if k not in images or not isinstance(images[k], str) or not images[k].strip():
                raise ServiceError(f"缺少图片URL: {k}")

        image_urls = [
            images["edit_image"].strip(),
            images["ref1"].strip(),
            images["ref2"].strip(),
            images["ref3"].strip(),
        ]

        payload = {
            "prompt": get_prompt("bigplate"),
            "images": image_urls,              # ✅ 必须是 array[string]
            "enable_sync_mode": True,          # ✅ 显式同步
            "enable_base64_output": False,
            "resolution": "1k",                # 可改 2k/4k
            # 同步模式下不要传 callback
        }

        result = post_edit(
            api_url=settings.API_URL,
            api_key=settings.API_KEY,
            payload=payload,
        )

        data = result.get("data") if isinstance(result, dict) else None
        if not isinstance(data, dict):
            logger.error("MCPP_bigplate invalid response: %s", result)
            raise ServiceError("上游返回格式异常")

        outputs = data.get("outputs") or []
        if outputs:
            logger.info("MCPP_bigplate success (sync)")
            return {"status": "success", "output": outputs[0], "mode": "sync"}

        # ✅ 同步没拿到 outputs：异步兜底
        result_url = (data.get("urls") or {}).get("get")
        if not result_url:
            logger.error("MCPP_bigplate no outputs and no result url: %s", result)
            raise ServiceError("模型未返回结果且缺少结果查询地址")

        final = wait_for_outputs(
            result_url=result_url,
            api_key=settings.API_KEY,
            timeout_seconds=180,
            poll_interval=1.0,
        )
        fdata = final.get("data") if isinstance(final, dict) else None
        foutputs = (fdata or {}).get("outputs") or []
        if not foutputs:
            logger.error("MCPP_bigplate async done but still no outputs: %s", final)
            raise ServiceError("模型未返回结果")

        logger.info("MCPP_bigplate success (async fallback)")
        return {"status": "success", "output": foutputs[0], "mode": "async"}

    except ServiceError:
        raise
    except Exception:
        logger.exception("MCPP_bigplate crashed")
        raise ServiceError("MCPP_bigplate internal error")
