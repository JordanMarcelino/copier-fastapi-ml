from app.api.routes import auth
from fastapi.routing import APIRouter

api_router = APIRouter()
api_router.include_router(auth.router)
