from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    """Requête de connexion"""
    email: EmailStr
    password: str = Field(..., min_length=8)


class RegisterRequest(BaseModel):
    """Requête d'inscription"""
    email: EmailStr
    nom: str = Field(..., min_length=2, max_length=100)
    prenom: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8)
    role: str = Field(..., pattern="^(agriculteur|agronome|chercheur)$")


class UtilisateurResponse(BaseModel):
    """Réponse utilisateur"""
    id_utilisateur: int
    email: str
    nom: str
    prenom: str
    role: str
    date_inscription: datetime
    
    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Réponse d'authentification avec tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UtilisateurResponse


class TokenRefreshRequest(BaseModel):
    """Requête de rafraîchissement de token"""
    refresh_token: str
