from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
import json

from app.core.config import settings
from app.core.database import create_all_tables
from app.routers import auth, diagnose, analyses, admin

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API de détection des maladies du cacaoyer via intelligence artificielle",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Initialiser les tables (à faire une fois au démarrage)
@app.on_event("startup")
async def startup_event():
    """Événement de démarrage"""
    logger.info("Démarrage de l'application")
    try:
        create_all_tables()
        logger.info("Base de données initialisée")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation: {e}")
    logger.info(f"Application {settings.APP_NAME} v{settings.APP_VERSION} prête")

@app.on_event("shutdown")
async def shutdown_event():
    """Événement d'arrêt"""
    logger.info("Arrêt de l'application")

# ── Configuration et Nettoyage du Middleware CORS 
raw_origins = settings.CORS_ORIGINS
origins = []

if isinstance(raw_origins, str):
    # Si le .env contient du JSON comme ["http://localhost:3003"]
    if raw_origins.startswith("[") and raw_origins.endswith("]"):
        try:
            origins = json.loads(raw_origins)
        except Exception:
            pass
    # Si le .env contient une liste séparée par des virgules
    else:
        origins = [o.strip() for o in raw_origins.split(",") if o.strip()]
elif isinstance(raw_origins, (list, tuple)):
    origins = list(raw_origins)

# Sécurité locale : On force l'inclusion de vos frontends de dev
local_frontends = ["http://localhost:3003", "http://127.0.0.1:3003", "http://localhost:3000"]
for frontend in local_frontends:
    if frontend not in origins:
        origins.append(frontend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes de santé 
@app.get("/health")
async def health_check():
    """Endpoint de vérification de santé"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": f"Bienvenue sur {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


# ── Inclusion des routers 
app.include_router(auth.router)
app.include_router(diagnose.router)
app.include_router(analyses.router)
app.include_router(admin.router)


# ── Gestion des erreurs 
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Gestionnaire global des exceptions"""
    logger.error(f"Erreur non gérée: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Une erreur interne s'est produite"}
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
    )