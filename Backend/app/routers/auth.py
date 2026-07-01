from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
)
from app.core.config import settings
from app.schemas.auth_schema import (
    LoginRequest,
    RegisterRequest,
    AuthResponse,
    UtilisateurResponse,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
async def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Enregistrer un nouvel utilisateur
    """
    # TODO: Vérifier que l'email n'existe pas
    # TODO: Créer l'utilisateur en base de données
    # TODO: Retourner les tokens
    
    # Placeholder pour la démo
    user = {
        "id_utilisateur": 1,
        "email": data.email,
        "nom": data.nom,
        "prenom": data.prenom,
        "role": data.role,
        "date_inscription": "2026-07-01T00:00:00",
    }
    
    access_token = create_access_token(
        data={"sub": str(user["id_utilisateur"])},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(data={"sub": str(user["id_utilisateur"])})
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UtilisateurResponse(**user)
    )


@router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Connexion utilisateur
    """
    # TODO: Récupérer l'utilisateur par email
    # TODO: Vérifier le mot de passe
    # TODO: Retourner les tokens
    
    # Placeholder pour la démo
    user = {
        "id_utilisateur": 1,
        "email": data.email,
        "nom": "Demo",
        "prenom": "User",
        "role": "agriculteur",
        "date_inscription": "2026-07-01T00:00:00",
    }
    
    access_token = create_access_token(
        data={"sub": str(user["id_utilisateur"])},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(data={"sub": str(user["id_utilisateur"])})
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UtilisateurResponse(**user)
    )


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Déconnexion (invalidation du token côté client)
    """
    return {"message": "Déconnexion réussie"}


@router.get("/me", response_model=UtilisateurResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Récupérer les infos de l'utilisateur actuel
    """
    # TODO: Récupérer les infos complètes de la base
    # Placeholder
    return {
        "id_utilisateur": current_user["user_id"],
        "email": "user@example.com",
        "nom": "User",
        "prenom": "Demo",
        "role": "agriculteur",
        "date_inscription": "2026-07-01T00:00:00",
    }


def get_db():
    """Dépendance pour la session de base de données"""
    # TODO: Implémenter la vraie connexion
    pass
