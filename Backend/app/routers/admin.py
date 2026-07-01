from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional

from app.core.security import get_current_user

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


async def check_admin(current_user: dict = Depends(get_current_user)):
    """Vérifier que l'utilisateur est administrateur"""
    # TODO: Récupérer le rôle de l'utilisateur et vérifier
    return current_user


@router.get("/users")
async def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(check_admin),
):
    """
    Lister tous les utilisateurs (admin seulement)
    """
    # TODO: Implémenter la requête
    return {
        "users": [],
        "total": 0,
        "page": page,
        "limit": limit,
    }


@router.put("/users/{id_utilisateur}")
async def update_user(
    id_utilisateur: int,
    data: dict,
    current_user: dict = Depends(check_admin),
):
    """
    Modifier un utilisateur (admin seulement)
    """
    # TODO: Implémenter la mise à jour
    return {"message": "Utilisateur modifié"}


@router.delete("/users/{id_utilisateur}")
async def delete_user(
    id_utilisateur: int,
    current_user: dict = Depends(check_admin),
):
    """
    Supprimer un utilisateur (admin seulement)
    """
    # TODO: Implémenter la suppression
    return {"message": "Utilisateur supprimé"}


@router.get("/stats")
async def get_stats(
    current_user: dict = Depends(check_admin),
):
    """
    Récupérer les statistiques globales (admin seulement)
    """
    # TODO: Implémenter les calculs de statistiques
    return {
        "total_utilisateurs": 5,
        "total_analyses": 42,
        "analyses_aujourd_hui": 12,
        "taux_detection": 0.78,
        "maladie_plus_frequente": "Rouille noire",
    }


@router.post("/modele")
async def deploy_model(
    file,
    current_user: dict = Depends(check_admin),
):
    """
    Déployer un nouveau modèle IA (admin seulement)
    """
    # TODO: Implémenter le déploiement
    return {"message": "Modèle déployé"}
