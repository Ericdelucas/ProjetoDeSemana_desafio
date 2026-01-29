from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from app.config import settings
from app.database import init_db
from app.routers.atendimento import router as atendimento_router
from app.routers.chat_ia import router as chat_router
from app.routers.roteamento import router as roteamento_router
from app.routers.unidades import router as unidades_router
from app.utils.logging_middleware import RequestTimingMiddleware


def create_app() -> FastAPI:
    """
    Criação da aplicação FastAPI.
    Mantém CORS robusto, middlewares e routers bem definidos.
    """
    app = FastAPI(
        title=getattr(settings, "app_name", "SmartSaúde SUS"),
        version="0.1.0",
    )

    # =========================
    # Middleware de logging/tempo
    # =========================
    app.add_middleware(RequestTimingMiddleware)

    # =========================
    # CORS (frontend Vite / React)
    # =========================
    default_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    cors_from_settings: list[str] = []
    raw = getattr(settings, "cors_origins", "") or ""
    if isinstance(raw, str) and raw.strip():
        cors_from_settings = [o.strip() for o in raw.split(",") if o.strip()]

    allow_origins = sorted(set(default_origins + cors_from_settings))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # =========================
    # Tratamento global de erro de banco
    # =========================
    @app.exception_handler(OperationalError)
    async def db_down_handler(request: Request, exc: OperationalError):
        return JSONResponse(
            status_code=503,
            content={
                "error": {
                    "code": "DB_UNAVAILABLE",
                    "message": "Banco MySQL indisponível. Tente novamente.",
                }
            },
        )

    # =========================
    # Healthcheck
    # =========================
    @app.get("/health", tags=["Health"])
    def health():
        return {"status": "ok"}

    # =========================
    # Routers da aplicação
    # =========================
    app.include_router(atendimento_router)
    app.include_router(chat_router)
    app.include_router(roteamento_router)
    app.include_router(unidades_router)

    # =========================
    # Debug de rotas (útil p/ front)
    # =========================
    @app.get("/_debug/routes", tags=["Debug"])
    def debug_routes():
        return sorted(
            [
                {
                    "path": r.path,
                    "name": r.name,
                    "methods": sorted(getattr(r, "methods", []) or []),
                }
                for r in app.router.routes
            ],
            key=lambda x: x["path"],
        )

    return app


# =========================
# Instância da aplicação
# =========================
app = create_app()

# =========================
# MVP: cria tabelas automaticamente
# =========================
init_db()

# Execução:
# uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload