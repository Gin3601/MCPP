import os
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from app.utils.http import post_edit, wait_for_outputs
from app.services.all_promot import get_prompt
from app.utils.logger import get_logger
from app.config import settings

logger = get_logger("MCPP_main")


class ServiceError(Exception):
    pass


# ====== 你可以用环境变量覆盖 ======
MEDIA_ROOT = os.getenv("MEDIA_ROOT", "./media")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").strip()  # 推荐配置，比如: http://192.168.1.10:8900


def _is_url(s: str) -> bool:
    s = (s or "").strip().lower()
    return s.startswith("http://") or s.startswith("https://")


def _ensure_media_root() -> Path:
    root = Path(MEDIA_ROOT)
    root.mkdir(parents=True, exist_ok=True)
    return root


def _guess_suffix(filename: str) -> str:
    suf = Path(filename or "").suffix.lower()
    return suf if suf else ".bin"


async def _save_uploadfile_to_media(upload_file: Any) -> str:
    """
    upload_file: FastAPI UploadFile (duck-typing)
    保存到 MEDIA_ROOT，返回文件名（相对路径）
    """
    root = _ensure_media_root()
    suffix = _guess_suffix(getattr(upload_file, "filename", "") or "")
    name = f"{uuid.uuid4().hex}{suffix}"
    dst = root / name

    # UploadFile 支持 async read
    with dst.open("wb") as f:
        while True:
            chunk = await upload_file.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)

    try:
        await upload_file.close()
    except Exception:
        pass

    return name


def _copy_local_path_to_media(local_path: str) -> str:
    """
    把本地文件复制到 MEDIA_ROOT，返回文件名
    """
    src = Path(local_path)
    if not src.exists() or not src.is_file():
        raise ServiceError(f"本地文件不存在: {local_path}")

    root = _ensure_media_root()
    suffix = src.suffix.lower() or ".bin"
    name = f"{uuid.uuid4().hex}{suffix}"
    dst = root / name

    # 直接读写复制，避免引入 shutil 也行
    with src.open("rb") as rf, dst.open("wb") as wf:
        while True:
            b = rf.read(1024 * 1024)
            if not b:
                break
            wf.write(b)
    return name


def _build_base_url(request: Any = None, base_url: Optional[str] = None) -> str:
    """
    优先级:
    1) 显式传 base_url
    2) 环境变量 PUBLIC_BASE_URL
    3) FastAPI Request.base_url
    """
    if base_url and base_url.strip():
        return base_url.strip().rstrip("/")
    if PUBLIC_BASE_URL:
        return PUBLIC_BASE_URL.rstrip("/")
    if request is not None:
        # FastAPI Request: str(request.base_url) like "http://127.0.0.1:8900/"
        return str(request.base_url).rstrip("/")
    raise ServiceError("缺少 base_url：请传入 base_url 或 request，或设置环境变量 PUBLIC_BASE_URL")


async def _to_accessible_url(
    item: Any,
    request: Any = None,
    base_url: Optional[str] = None,
) -> Optional[str]:
    """
    把任意输入变成模型可访问的 URL
    支持:
    - http(s)://...  直接返回
    - UploadFile     保存到 media 并返回 {base}/media/<name>
    - 本地路径        复制到 media 并返回 {base}/media/<name>
    """
    if isinstance(item, str) and item.strip():
        s = item.strip()
        if _is_url(s):
            return s
        # 不是 URL，当成本地路径
        name = _copy_local_path_to_media(s)
        base = _build_base_url(request=request, base_url=base_url)
        return f"{base}/media/{name}"

    # FastAPI UploadFile (duck typing: 有 filename + read)
    if hasattr(item, "read") and hasattr(item, "filename"):
        name = await _save_uploadfile_to_media(item)
        base = _build_base_url(request=request, base_url=base_url)
        return f"{base}/media/{name}"

    return None


async def _normalize_images(
    images: Union[List[Any], Dict[str, Any]],
    request: Any = None,
    base_url: Optional[str] = None,
) -> List[str]:
    """
    允许接口层传：
    - list[str|UploadFile|path]
    - dict：{"edit_image": ..., "ref1": ..., "ref2": ..., "ref3": ...}
    - dict：{"images": [...]}
    最终统一返回 array[string] 的可访问 URL 列表
    """
    items: List[Any] = []

    if isinstance(images, list):
        items = images
    elif isinstance(images, dict):
        # 兼容结构：{"edit_image": "...", "ref1": "...", ...}
        keys = ["edit_image", "ref1", "ref2", "ref3"]
        for k in keys:
            if k in images:
                items.append(images.get(k))
        # 也允许 dict 里直接有 "images": [...]
        if not any(items) and isinstance(images.get("images"), list):
            items = images["images"]
    else:
        items = []

    urls: List[str] = []
    for it in items:
        u = await _to_accessible_url(it, request=request, base_url=base_url)
        if u:
            urls.append(u)

    # 去重（保序）
    seen = set()
    dedup = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            dedup.append(u)
    return dedup


async def run(images: Union[List[Any], Dict[str, Any]], request: Any = None, base_url: Optional[str] = None):
    """
    ✅ 可直接运行版本：
    - images 可以是 URL / UploadFile / 本地路径
    - 如果是 UploadFile/本地路径：会保存到 MEDIA_ROOT 并构造成 base_url/media/xxx
    - 同步拿不到 outputs：自动异步轮询兜底
    """
    logger.info("MCPP_main start")

    try:
        image_urls = await _normalize_images(images, request=request, base_url=base_url)
        if len(image_urls) < 2:
            raise ServiceError("至少需要 2 张图片：edit_image + 至少 1 张 ref（支持 URL/UploadFile/本地路径）")

        payload = {
            "prompt": get_prompt("main"),
            "images": image_urls,              # ✅ 必须是 array[string]
            "enable_sync_mode": True,          # ✅ 显式开启同步
            "enable_base64_output": False,
            "resolution": "1k",                # ✅ 可选：1k/2k/4k
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

        outputs = data.get("outputs") or []
        if outputs:
            logger.info("MCPP_main success (sync)")
            return {"status": "success", "outputs": outputs, "mode": "sync"}

        # 同步没拿到 outputs：异步兜底
        result_url = (data.get("urls") or {}).get("get")
        if not result_url:
            logger.error("MCPP_main no outputs and no result url: %s", result)
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
            logger.error("MCPP_main async done but still no outputs: %s", final)
            raise ServiceError("模型未返回结果")

        logger.info("MCPP_main success (async fallback)")
        return {"status": "success", "outputs": foutputs, "mode": "async"}

    except ServiceError:
        raise
    except Exception:
        logger.exception("MCPP_main crashed")
        raise ServiceError("MCPP_main internal error")
