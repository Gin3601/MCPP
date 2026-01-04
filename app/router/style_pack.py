from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Query

from app.utils.logger import get_logger
from app.services.image_store import save_4_images, ServiceError as StoreError
from app.services.style_pack import run_style_pack, ALLOWED_TASKS

logger = get_logger("style_pack_route")

router = APIRouter(prefix="/run", tags=["StylePack"])


@router.post("/style-pack/upload")
async def style_pack_upload(
    request: Request,
    edit_image: UploadFile = File(...),
    ref1: UploadFile = File(...),
    ref2: UploadFile = File(...),
    ref3: UploadFile = File(...),
    tasks: str = Query(
        "main,ground,ground2,smallplate,bigplate,batch",
        description="逗号分隔任务名，只跑这些以减少消耗",
    ),
):
    # 解析 tasks
    want = [t.strip().lower() for t in tasks.split(",") if t.strip()]
    chosen = [t for t in want if t in ALLOWED_TASKS]
    if not chosen:
        raise HTTPException(status_code=400, detail=f"tasks 参数无效，可选：{sorted(ALLOWED_TASKS)}")

    # ① 保存一次：UploadFile -> media -> URL
    try:
        urls = await save_4_images(edit_image, ref1, ref2, ref3, request=request)
    except StoreError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("save_4_images failed")
        raise HTTPException(status_code=500, detail="save images failed")

    # ② 跑 chosen
    try:
        results = await run_style_pack(urls, tasks=chosen, request=request)
    except Exception as e:
        # 如果你希望“任何业务错误都返回400”，可在这里做更精细判断
        logger.exception("run_style_pack crashed")
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "inputs": urls, "tasks": chosen, "results": results}
