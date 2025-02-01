import warnings

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.settings.app_factory import app
from app.settings.config import settings
from app.settings.middlewares import HTTP_MIDDLEWARES

warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*TLS in TLS.*")
app = app

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
for mw in HTTP_MIDDLEWARES:
    app.add_middleware(BaseHTTPMiddleware, dispatch=mw)
