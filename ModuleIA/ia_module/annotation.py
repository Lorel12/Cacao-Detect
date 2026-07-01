"""
annotation.py
-------------
Dessine les boîtes englobantes et les labels de diagnostic
directement sur l'image originale.

Retourne l'image annotée sous forme de bytes (pour upload S3)
ou la sauvegarde sur disque.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Union

from config import (
    ANNOTATION_COLORS, BOX_THICKNESS, FONT_SCALE, LABEL_PADDING
)


# ── Couleurs et styles ────────────────────────────────────────────────────────

DEFAULT_COLOR = (100, 100, 100)  # Gris pour classes non référencées
FONT = cv2.FONT_HERSHEY_SIMPLEX


def _get_color(class_name: str) -> tuple:
    """Retourne la couleur BGR associée à une classe."""
    return ANNOTATION_COLORS.get(class_name, DEFAULT_COLOR)


# ── Dessin d'une détection ────────────────────────────────────────────────────

def _draw_detection(image: np.ndarray, detection: dict) -> np.ndarray:
    """
    Dessine une boîte englobante et son label sur l'image.

    Paramètre :
        detection : dict produit par inference.parse_results()
                    {class_name, confidence, bbox: {x1, y1, x2, y2}}

    Retourne l'image modifiée (in-place).
    """
    bbox        = detection["bbox"]
    class_name  = detection["class_name"]
    confidence  = detection["confidence"]
    color       = _get_color(class_name)

    x1, y1 = bbox["x1"], bbox["y1"]
    x2, y2 = bbox["x2"], bbox["y2"]

    # Boîte englobante
    cv2.rectangle(image, (x1, y1), (x2, y2), color, BOX_THICKNESS)

    # Texte du label : "classe (xx%)"
    label = f"{class_name.replace('_', ' ')} ({confidence * 100:.0f}%)"
    (text_w, text_h), baseline = cv2.getTextSize(
        label, FONT, FONT_SCALE, 1
    )

    # Fond du label (rectangle de couleur)
    label_bg_y1 = max(y1 - text_h - 2 * LABEL_PADDING, 0)
    label_bg_y2 = y1
    cv2.rectangle(
        image,
        (x1, label_bg_y1),
        (x1 + text_w + 2 * LABEL_PADDING, label_bg_y2),
        color,
        cv2.FILLED,
    )

    # Texte en blanc sur le fond coloré
    cv2.putText(
        image,
        label,
        (x1 + LABEL_PADDING, y1 - LABEL_PADDING),
        FONT,
        FONT_SCALE,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )

    return image


# ── Annotation complète ───────────────────────────────────────────────────────

def annotate_image(image_bytes: bytes, detections: list) -> bytes:
    """
    Applique toutes les annotations (boîtes + labels) à l'image originale.

    Paramètres :
        image_bytes : bytes bruts de l'image originale (JPEG ou PNG)
        detections  : liste de dicts produite par inference.parse_results()

    Retourne :
        bytes de l'image annotée encodée en JPEG.
    """
    # Décodage depuis bytes (OpenCV lit en BGR)
    buffer = np.frombuffer(image_bytes, dtype=np.uint8)
    image  = cv2.imdecode(buffer, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Impossible de décoder l'image pour l'annotation.")

    # Dessin de chaque détection
    for detection in detections:
        image = _draw_detection(image, detection)

    # Ajout d'un filigrane discret
    _add_watermark(image)

    # Ré-encodage en JPEG
    success, encoded = cv2.imencode(
        ".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 92]
    )
    if not success:
        raise RuntimeError("Échec de l'encodage de l'image annotée.")

    return encoded.tobytes()


def annotate_and_save(image_input: Union[str, Path, bytes],
                      detections: list,
                      output_path: Union[str, Path]) -> Path:
    """
    Annote l'image et la sauvegarde sur disque.

    Pratique pour les tests locaux, sans passer par S3.

    Retourne le chemin du fichier sauvegardé.
    """
    if isinstance(image_input, (str, Path)):
        with open(image_input, "rb") as f:
            image_bytes = f.read()
    else:
        image_bytes = image_input

    annotated_bytes = annotate_image(image_bytes, detections)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(annotated_bytes)

    return output_path


# ── Filigrane ─────────────────────────────────────────────────────────────────

def _add_watermark(image: np.ndarray) -> None:
    """
    Ajoute un filigrane « CacaoDetect » discret en bas à droite de l'image.
    Modifie l'image en place.
    """
    text    = "CacaoDetect"
    scale   = 0.4
    color   = (200, 200, 200)
    h, w    = image.shape[:2]
    (tw, th), _ = cv2.getTextSize(text, FONT, scale, 1)
    cv2.putText(
        image, text,
        (w - tw - 8, h - 8),
        FONT, scale, color, 1, cv2.LINE_AA
    )
