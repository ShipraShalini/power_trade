import sentry_sdk
from fastapi import FastAPI
from fastapi.exception_handlers import http_exception_handler
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise

from power import api
from power.exception_handler import EXCEPTION_HANDLERS_DICT
from power.settings import DB_MODULES, settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    openapi_url=f"/{settings.PROJECT_NAME}/openapi.json",
    exception_handlers=EXCEPTION_HANDLERS_DICT,
    default_response_class=JSONResponse,
)

# Refer: https://github.com/tiangolo/fastapi/issues/4071#issuecomment-950833326
app.add_middleware(
    ServerErrorMiddleware,
    handler=http_exception_handler,
)

sentry_sdk.init(settings.SENTRY_DSN, environment=settings.ENVIRONMENT, attach_stacktrace=True)
app.add_middleware(SentryAsgiMiddleware)

register_tortoise(
    app,
    db_url=settings.DB_URL,
    modules=DB_MODULES,
    add_exception_handlers=True,
    generate_schemas=True,  # todo: use aerich to generate enum
)


app.include_router(router=api.router)


@app.get("/healthcheck")
async def healthcheck() -> JSONResponse:
    return JSONResponse(
        content={
            "success": True,
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "service_name": settings.PROJECT_NAME,
        }
    )
