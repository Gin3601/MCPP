import os
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.staticfiles import StaticFiles

from app.utils.logger import get_logger

# 你的 service（这些 run() 都是 async def）
from app.services.MCPP_main import run as main_run, ServiceError
from app.services.MCPP_information import run as information_run
from app.services.MCPP_bigplate import run as bigplate_run
from app.services.MCPP_smallplate import run as smallplate_run
from app.services.MCPP_ground import run as ground_run
from app.services.MCPP_ground2 import run as ground2_run
from app.services.MCPP_batch import run as batch_run

# 你的整合接口路由（注意：你的目录叫 router，不是 routes）
from app.router.style_pack import router as style_pack_router

logger = get_logger("main")

app = FastAPI(title="MCPP Image API")

# ✅ 挂载 /media：让保存到 MEDIA_ROOT 的图片可以被 URL 访问到
MEDIA_ROOT = os.getenv("MEDIA_ROOT", "./media")
Path(MEDIA_ROOT).mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")

# ✅ 注册整合接口
app.include_router(style_pack_router)


def collect_images(edit_image: UploadFile, ref1: UploadFile, ref2: UploadFile, ref3: UploadFile) -> dict:
    """
    ✅ 不要 base64，直接传 UploadFile
    由 MCPP_xxx.run 内部保存到 media 并生成 URL
    """
    return {
        "edit_image": edit_image,
        "ref1": ref1,
        "ref2": ref2,
        "ref3": ref3,
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/run/main/upload")
async def run_main_upload(
    request: Request,
    edit_image: UploadFile = File(...),
    ref1: UploadFile = File(...),
    ref2: UploadFile = File(...),
    ref3: UploadFile = File(...),
):
    images = collect_images(edit_image, ref1, ref2, ref3)
    try:
        return await main_run(images, request=request)
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("run_main_upload crashed")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/run/information/upload")
async def run_information_upload(
    request: Request,
    edit_image: UploadFile = File(...),
    ref1: UploadFile = File(...),
    ref2: UploadFile = File(...),
    ref3: UploadFile = File(...),
):
    images = collect_images(edit_image, ref1, ref2, ref3)
    try:
        return await information_run(images, request=request)
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("run_information_upload crashed")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/run/bigplate/upload")
async def run_bigplate_upload(
    request: Request,
    edit_image: UploadFile = File(...),
    ref1: UploadFile = File(...),
    ref2: UploadFile = File(...),
    ref3: UploadFile = File(...),
):
    images = collect_images(edit_image, ref1, ref2, ref3)
    try:
        return await bigplate_run(images, request=request)
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("run_bigplate_upload crashed")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/run/smallplate/upload")
async def run_smallplate_upload(
    request: Request,
    edit_image: UploadFile = File(...),
    ref1: UploadFile = File(...),
    ref2: UploadFile = File(...),
    ref3: UploadFile = File(...),
):
    images = collect_images(edit_image, ref1, ref2, ref3)
    try:
        return await smallplate_run(images, request=request)
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("run_smallplate_upload crashed")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/run/ground/upload")
async def run_ground_upload(
    request: Request,
    edit_image: UploadFile = File(...),
    ref1: UploadFile = File(...),
    ref2: UploadFile = File(...),
    ref3: UploadFile = File(...),
):
    images = collect_images(edit_image, ref1, ref2, ref3)
    try:
        return await ground_run(images, request=request)
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("run_ground_upload crashed")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/run/ground2/upload")
async def run_ground2_upload(
    request: Request,
    edit_image: UploadFile = File(...),
    ref1: UploadFile = File(...),
    ref2: UploadFile = File(...),
    ref3: UploadFile = File(...),
):
    images = collect_images(edit_image, ref1, ref2, ref3)
    try:
        return await ground2_run(images, request=request)
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("run_ground2_upload crashed")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/run/batch/upload")
async def run_batch_upload(
    request: Request,
    edit_image: UploadFile = File(...),
    ref1: UploadFile = File(...),
    ref2: UploadFile = File(...),
    ref3: UploadFile = File(...),
):
    images = collect_images(edit_image, ref1, ref2, ref3)
    try:
        return await batch_run(images, request=request)
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("run_batch_upload crashed")
        raise HTTPException(status_code=500, detail="Internal server error")
