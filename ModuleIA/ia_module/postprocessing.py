"""
postprocessing.py
-----------------
Post-traitement des détections brutes produites par inference.py.

Fonctions :
  - Calcul du niveau de gravité selon la surface détectée / surface totale
  - Extraction du diagnostic principal (classe la plus probable)
  - Construction de la réponse JSON finale du module IA
"""

from typing import Optional
from config import GRAVITY_THRESHOLDS, CLASS_NAMES


# ── Calcul du niveau de gravité ───────────────────────────────────────────────

def compute_gravity(detections: list,
                    image_width: int,
                    image_height: int) -> str:
    """
    Calcule le niveau de gravité de la maladie détectée.

    Méthode (cahier de conception, section VI.2) :
        Ratio = Σ surfaces détectées / surface totale de l'image

    Seuils :
        Faible  : ratio < 15 %  → surveillance, traitement préventif
        Modéré  : 15 % ≤ ratio < 40 % → traitement curatif localisé
        Élevé   : ratio ≥ 40 % → traitement intensif, alerte agronomique

    Paramètres :
        detections   : liste de dicts produite par inference.parse_results()
        image_width  : largeur de l'image originale (px)
        image_height : hauteur de l'image originale (px)

    Retourne :
        "faible" | "modere" | "eleve"
    """
    image_area = image_width * image_height
    if image_area == 0:
        return "faible"

    # On exclut les détections de classe "sain" du calcul de gravité
    total_detected_area = 0
    for det in detections:
        if det["class_name"] == "sain":
            continue
        bbox = det["bbox"]
        total_detected_area += bbox["width"] * bbox["height"]

    ratio = total_detected_area / image_area

    if ratio < GRAVITY_THRESHOLDS["faible"]:
        return "faible"
    elif ratio < GRAVITY_THRESHOLDS["modere"]:
        return "modere"
    else:
        return "eleve"


# ── Extraction du diagnostic principal ────────────────────────────────────────

def extract_primary_diagnosis(detections: list) -> Optional[dict]:
    """
    Extrait la détection principale (score de confiance le plus élevé).

    Si aucune maladie n'est détectée, retourne None
    (la plante sera considérée comme saine).

    Retourne :
        dict avec class_name, confidence et bbox,
        ou None si pas de maladie détectée.
    """
    # Les détections sont déjà triées par confiance décroissante (inference.py)
    disease_detections = [
        d for d in detections if d["class_name"] != "sain"
    ]
    return disease_detections[0] if disease_detections else None


# ── Construction de la réponse finale ─────────────────────────────────────────

def build_diagnostic_result(detections: list,
                             original_shape: tuple,
                             image_annotated_url: str = "") -> dict:
    """
    Construit le dictionnaire de résultat final du module IA,
    prêt à être sérialisé en JSON par FastAPI.

    Structure de sortie :
    {
        "maladie"            : str,   # Nom de la maladie (ou "sain")
        "gravite"            : str,   # "faible" | "modere" | "eleve"
        "confiance"          : float, # Score de confiance principal [0, 1]
        "image_annotee_url"  : str,   # URL S3 de l'image annotée
        "toutes_detections"  : list,  # Liste complète des détections
        "nb_zones_detectees" : int,   # Nombre de zones malades identifiées
    }

    Paramètres :
        detections          : liste produite par inference.parse_results()
        original_shape      : (hauteur, largeur) de l'image originale
        image_annotated_url : URL S3 de l'image annotée (fourni par annotation.py)
    """
    orig_h, orig_w = original_shape
    primary = extract_primary_diagnosis(detections)
    gravity = compute_gravity(detections, orig_w, orig_h)

    if primary is None:
        # Aucune maladie détectée → plante saine
        maladie   = "sain"
        confiance = 1.0 if not detections else detections[0]["confidence"]
        gravity   = "faible"
    else:
        maladie   = primary["class_name"]
        confiance = primary["confidence"]

    disease_detections = [
        d for d in detections if d["class_name"] != "sain"
    ]

    return {
        "maladie"            : maladie,
        "gravite"            : gravity,
        "confiance"          : confiance,
        "image_annotee_url"  : image_annotated_url,
        "toutes_detections"  : detections,
        "nb_zones_detectees" : len(disease_detections),
    }
