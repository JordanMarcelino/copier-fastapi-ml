from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core import limiter, logger, settings
from app.core.db import init_db
from app.schemas.web_response import Info, WebResponse


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Migrate table
        init_db()
    except Exception as exc:
        logger.error(exc)

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

# Rate limiter
app.state.limiter = limiter


@app.exception_handler(HTTPException)
async def error_handler(request: Request, exc: HTTPException):
    logger.error(exc)
    return JSONResponse(
        content=WebResponse[None](
            info=Info(status=False, message=exc.detail),
        ).model_dump(),
        status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    logger.error(exc)
    return JSONResponse(
        content=WebResponse[None](
            info=Info(status=False, meta=exc.errors(), message="Unprocessable entity"),
        ).model_dump(),
        status_code=422,
    )


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
