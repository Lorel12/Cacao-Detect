"""
ia_module
---------
Module d'intelligence artificielle de CacaoDetect.

API publique exposée (importable par ia_service.py du backend) :
    from ia_module import run_pipeline
"""

from .inference     import model_singleton
from .preprocessing import preprocess
from .inference     import run_inference_with_timeout, parse_results
from .postprocessing import build_diagnostic_result
from .annotation    import annotate_image


def run_pipeline(image_bytes: bytes) -> dict:
    """
    Point d'entrée unique du module IA.

    Exécute le pipeline complet :
        bytes → prétraitement → inférence → post-traitement → annotation

    Paramètre :
        image_bytes : bytes bruts de l'image (upload HTTP)

    Retourne :
        dict {maladie, gravite, confiance, image_annotee_bytes, toutes_detections}

    Note :
        L'upload de l'image annotée sur S3 est géré par storage_service.py
        côté backend. Ce module retourne les bytes de l'image annotée.
    """
    # 1. Prétraitement
    preprocessed, original_shape = preprocess(image_bytes)

    # 2. Inférence (avec timeout + retries)
    raw_results = run_inference_with_timeout(preprocessed)

    # 3. Parsing des détections
    detections = parse_results(raw_results, original_shape)

    # 4. Annotation de l'image originale
    annotated_bytes = annotate_image(image_bytes, detections)

    # 5. Construction du résultat final
    result = build_diagnostic_result(
        detections=detections,
        original_shape=original_shape,
        image_annotated_url="",  # L'URL S3 sera ajoutée par ia_service.py
    )
    result["image_annotee_bytes"] = annotated_bytes

    return result
