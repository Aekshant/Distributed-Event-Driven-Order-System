from fastapi import APIRouter

from app.httpServer.router.order_router import router as order_router
router = APIRouter()

router.include_router(
    order_router
)