import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes.health import router as health_router
from app.api.routes.insights import router as insights_router
from app.api.routes.agents import router as agents_router
from app.api import decision, advisory, chat
from app.api.forecast import router as forecast_router
from app.core.config import settings
from app.core.exceptions import AERISException
from app.core.logging import logger
from app.core.logging_config import configure_logging

configure_logging()

app = FastAPI(title=settings.app_name, version=settings.api_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount exports directory for public KML serving (e.g. Google Maps API KML Layer)
exports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "exports"))
os.makedirs(os.path.join(exports_dir, "kml"), exist_ok=True)
app.mount("/exports", StaticFiles(directory=exports_dir), name="exports")


@app.exception_handler(AERISException)
async def aeris_exception_handler(request, exc: AERISException):
    logger.warning("AERIS exception: %s", str(exc))
    return {"detail": str(exc)}


app.include_router(health_router, prefix="/api")
app.include_router(insights_router, prefix="/api")
app.include_router(agents_router)
app.include_router(forecast_router)
app.include_router(decision.router)
app.include_router(advisory.router)
app.include_router(chat.router)

