#负责：UploadFile → 保存到 MEDIA_ROOT → 返回可访问 URL（一次性）
import os
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

MEDIA_ROOT = os.getenv("MEDIA_ROOT", "./media")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").strip()


class ServiceError(Exception):
    pass


def _ensure_media_root() -> Path:
    root = Path(MEDIA_ROOT)
    root.mkdir(parents=True, exist_ok=True)
    return root


def _guess_suffix(filename: str) -> str:
    suf = Path(filename or "").suffix.lower()
    return suf if suf else ".bin"


def _build_base_url(request: Any = None, base_url: Optional[str] = None) -> str:
    if base_url and base_url.strip():
        return base_url.strip().rstrip("/")
    if PUBLIC_BASE_URL:
        return PUBLIC_BASE_URL.rstrip("/")
    if request is not None:
        return str(request.base_url).rstrip("/")
    raise ServiceError("缺少 base_url：请传 request 或设置环境变量 PUBLIC_BASE_URL")


async def save_uploadfile_as_url(
    upload_file: Any,
    request: Any = None,
    base_url: Optional[str] = None,
) -> str:
    """
    UploadFile -> 保存到 MEDIA_ROOT -> 返回 {base}/media/<uuid>.<ext>
    """
    root = _ensure_media_root()
    suffix = _guess_suffix(getattr(upload_file, "filename", "") or "")
    name = f"{uuid.uuid4().hex}{suffix}"
    dst = root / name

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

    base = _build_base_url(request=request, base_url=base_url)
    return f"{base}/media/{name}"


async def save_4_images(
    edit_image: Any,
    ref1: Any,
    ref2: Any,
    ref3: Any,
    request: Any = None,
    base_url: Optional[str] = None,
) -> Dict[str, str]:
    """
    一次性保存4张图，返回 URL 映射
    """
    return {
        "edit": await save_uploadfile_as_url(edit_image, request=request, base_url=base_url),
        "ref1": await save_uploadfile_as_url(ref1, request=request, base_url=base_url),
        "ref2": await save_uploadfile_as_url(ref2, request=request, base_url=base_url),
        "ref3": await save_uploadfile_as_url(ref3, request=request, base_url=base_url),
    }
