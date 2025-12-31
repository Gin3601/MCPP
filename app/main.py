from fastapi import FastAPI, UploadFile, File
import base64
from app.services.MCPP_main import run as main_run
from app.services.MCPP_bigplate import run as bigplate_run
from app.services.MCPP_ground import run as ground_run
from app.services.MCPP_information import run as information_run
from app.services.MCPP_smallplate import run as smallplate_run
from app.services.MCPP_batch import run as batch_run
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.services.MCPP_main import run as main_run, ServiceError
from app.utils.logger import get_logger

logger = get_logger()

app = FastAPI(title="MCPP Image API")

def to_base64(file: UploadFile) -> str:
    return base64.b64encode(file.file.read()).decode("utf-8")


def collect_images(
    edit_image: UploadFile,
    ref1: UploadFile,
    ref2: UploadFile,
    ref3: UploadFile,
) -> dict:
    return {
        "edit_image": to_base64(edit_image),
        "ref1": to_base64(ref1),
        "ref2": to_base64(ref2),
        "ref3": to_base64(ref3),
    }

@app.post("/run/main/upload")
def run_main_upload(
    edit_image: UploadFile = File(...),
    ref1: UploadFile = File(...),
    ref2: UploadFile = File(...),
    ref3: UploadFile = File(...),
):
    images = collect_images(edit_image, ref1, ref2, ref3)
    try:
        return main_run(images)

    except ServiceError as e:
        # 👉 业务失败（模型问题、参数问题）
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception:
        # 👉 真正的系统错误
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )

@app.post("/run/information/upload")
def run_information_upload(
    edit_image: UploadFile = File(...),
    ref1: UploadFile = File(...),
    ref2: UploadFile = File(...),
    ref3: UploadFile = File(...),
):
    images = collect_images(edit_image, ref1, ref2, ref3)
    
    try:
        return information_run(images)
    except ServiceError as e:
        # 👉 业务失败（模型问题、参数问题）
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception:
        # 👉 真正的系统错误
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )


@app.post("/run/bigplate/upload")
def run_bigplate_upload(
    edit_image: UploadFile = File(...),
    ref1: UploadFile = File(...),
    ref2: UploadFile = File(...),
    ref3: UploadFile = File(...),
):
    images = collect_images(edit_image, ref1, ref2, ref3)
    try:
        return bigplate_run(images)
    except ServiceError as e:
        # 👉 业务失败（模型问题、参数问题）
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception:
        # 👉 真正的系统错误
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )


@app.post("/run/smallplate/upload")
def run_smallplate_upload(
    edit_image: UploadFile = File(...),
    ref1: UploadFile = File(...),
    ref2: UploadFile = File(...),
    ref3: UploadFile = File(...),
):
    images = collect_images(edit_image, ref1, ref2, ref3)
    try:
        return smallplate_run(images)
    except ServiceError as e:
        # 👉 业务失败（模型问题、参数问题）
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception:
        # 👉 真正的系统错误
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )   

@app.post("/run/ground/upload")
def run_ground_upload(
    edit_image: UploadFile = File(...),
    ref1: UploadFile = File(...),
    ref2: UploadFile = File(...),
    ref3: UploadFile = File(...),
):
    images = collect_images(edit_image, ref1, ref2, ref3)
    try:
        return ground_run(images)
    except ServiceError as e:
        # 👉 业务失败（模型问题、参数问题）
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception:
        # 👉 真正的系统错误
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )       


@app.post("/run/batch/upload")
def run_batch_upload(
    edit_image: UploadFile = File(...),
    ref1: UploadFile = File(...),
    ref2: UploadFile = File(...),
    ref3: UploadFile = File(...),
):
    images = collect_images(edit_image, ref1, ref2, ref3)
    try:
        return batch_run(images)
    except ServiceError as e:
        # 👉 业务失败（模型问题、参数问题）
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception:
        # 👉 真正的系统错误
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )   
