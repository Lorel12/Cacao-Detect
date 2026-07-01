from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from sqlalchemy.orm import Session
import logging

from app.services.ia_service import ia_service
from app.services.storage_service import storage_service
from app.core.security import get_current_user
from app.schemas.diagnostic_schema import AnalyseSchema

router = APIRouter(prefix="/api/v1/diagnose", tags=["diagnose"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=AnalyseSchema)
async def upload_and_analyze(
    file: UploadFile = File(...),
    notes: str = None,
    current_user: dict = Depends(get_current_user),
):
    """
    Upload une image et lance l'analyse IA
    """
    try:
        # Valider le fichier
        file_content = await file.read()
        valid, msg = storage_service.validate_file(file.filename, len(file_content))
        if not valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
        
        # Sauvegarder le fichier
        file_path = storage_service.save_file(file_content, file.filename)
        
        # Analyser l'image
        diagnosis_result = ia_service.analyze_image(file_path)
        
        # Annoter l'image si nécessaire
        annotated_path = None
        if diagnosis_result.get("bbox"):
            annotated_path = ia_service.annotate_image(file_path, diagnosis_result["bbox"])
        
        # TODO: Sauvegarder en base de données
        # Placeholder
        return {
            "id_analyse": 1,
            "date_heure": "2026-07-01T00:00:00",
            "statut": "termine",
            "duree_traitement_s": diagnosis_result.get("temps_inference_ms", 0) / 1000,
            "flag_avertissement": diagnosis_result.get("confiance", 1.0) < 0.6,
            "diagnostic": {
                "id_diagnostic": 1,
                "maladie": None,
                "niveau_gravite": None,
                "score_confiance": diagnosis_result.get("confiance", 0.0),
                "bbox": diagnosis_result.get("bbox"),
                "chemin_image_annotee": annotated_path,
                "flag_avertissement": False,
            }
        }
    
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
