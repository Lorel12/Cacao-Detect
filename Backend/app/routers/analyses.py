from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.security import get_current_user
from app.schemas.diagnostic_schema import (
    AnalyseSchema,
    AnalysesListResponseSchema,
    AnalyseListItemSchema,
    GraviteEnum,
)

router = APIRouter(prefix="/api/v1/analyses", tags=["analyses"])


@router.get("/", response_model=AnalysesListResponseSchema)
async def list_analyses(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    maladie: Optional[str] = None,
    gravite: Optional[GraviteEnum] = None,
    date_debut: Optional[str] = None,
    date_fin: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
):
    """
    Lister les analyses de l'utilisateur avec filtres
    """
    # TODO: Implémenter la requête en base avec filtres
    # Placeholder
    return {
        "analyses": [
            {
                "id_analyse": 1,
                "date_heure": "2026-07-01T10:00:00",
                "statut": "termine",
                "maladie_nom": None,
                "niveau_gravite": None,
                "score_confiance": 0.92,
                "image_annotee_url": None,
            }
        ],
        "total": 1,
        "page": page,
        "limit": limit,
    }


@router.get("/{id_analyse}", response_model=AnalyseSchema)
async def get_analyse(
    id_analyse: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Récupérer le détail d'une analyse
    """
    # TODO: Implémenter la récupération en base
    # Placeholder
    return {
        "id_analyse": id_analyse,
        "date_heure": "2026-07-01T10:00:00",
        "statut": "termine",
        "duree_traitement_s": 2.5,
        "flag_avertissement": False,
        "diagnostic": {
            "id_diagnostic": 1,
            "maladie": None,
            "niveau_gravite": None,
            "score_confiance": 0.92,
            "bbox": None,
            "chemin_image_annotee": None,
            "flag_avertissement": False,
        }
    }


@router.delete("/{id_analyse}")
async def delete_analyse(
    id_analyse: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Supprimer une analyse
    """
    # TODO: Implémenter la suppression
    return {"message": "Analyse supprimée"}


@router.get("/{id_analyse}/export")
async def export_analyse_pdf(
    id_analyse: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Exporter une analyse en PDF
    """
    # TODO: Implémenter l'export PDF
    # Placeholder - retourner un PDF vide pour la démo
    return {"message": "Export PDF en cours de développement"}
