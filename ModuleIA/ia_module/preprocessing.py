"""
preprocessing.py
----------------
Prétraitement des images avant inférence YOLOv8.

Pipeline appliqué (conforme au cahier de conception) :
  1. Lecture de l'image (fichier ou bytes)
  2. Redimensionnement à 640 × 640 px
  3. Normalisation des pixels sur [0, 1]
  4. Conversion BGR → RGB
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Union

from config import IMG_SIZE, NORMALIZE, COLOR_MODE


def load_image_from_bytes(image_bytes: bytes) -> np.ndarray:
    """
    Charge une image à partir de bytes bruts (ex. upload HTTP multipart).

    Retourne un tableau NumPy en BGR (format natif OpenCV).
    """
    buffer = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(
            "Impossible de décoder l'image. "
            "Vérifiez que le fichier est un JPEG ou PNG valide."
        )
    return image


def load_image_from_path(image_path: Union[str, Path]) -> np.ndarray:
    """
    Charge une image depuis le disque.

    Retourne un tableau NumPy en BGR.
    """
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Image introuvable : {image_path}")
    return image


def resize_image(image: np.ndarray,
                 target_size: int = IMG_SIZE) -> np.ndarray:
    """
    Redimensionne l'image à (target_size × target_size) px.

    Utilise l'interpolation INTER_LINEAR (bon compromis vitesse/qualité).
    """
    return cv2.resize(image, (target_size, target_size),
                      interpolation=cv2.INTER_LINEAR)


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalise les valeurs de pixels de [0, 255] vers [0.0, 1.0].

    Retourne un tableau float32.
    """
    return image.astype(np.float32) / 255.0


def convert_bgr_to_rgb(image: np.ndarray) -> np.ndarray:
    """
    Convertit une image BGR (OpenCV) en RGB.

    YOLOv8 (via Ultralytics) attend des images en RGB.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def preprocess(image_input: Union[bytes, str, Path, np.ndarray]) -> np.ndarray:
    """
    Pipeline complet de prétraitement.

    Accepte :
        - bytes         → upload HTTP
        - str / Path    → chemin fichier
        - np.ndarray    → image déjà chargée en BGR

    Retourne :
        np.ndarray de shape (640, 640, 3), dtype float32, espace RGB.

    Exemple :
        >>> with open("feuille.jpg", "rb") as f:
        ...     img_preprocessed = preprocess(f.read())
        >>> img_preprocessed.shape
        (640, 640, 3)
    """
    # 1. Chargement
    if isinstance(image_input, bytes):
        image = load_image_from_bytes(image_input)
    elif isinstance(image_input, (str, Path)):
        image = load_image_from_path(image_input)
    elif isinstance(image_input, np.ndarray):
        image = image_input.copy()
    else:
        raise TypeError(
            f"Type d'entrée non supporté : {type(image_input)}. "
            "Attendu : bytes, str, Path ou np.ndarray."
        )

    original_shape = image.shape[:2]  # (hauteur, largeur) avant redim.

    # 2. Redimensionnement
    image = resize_image(image, target_size=IMG_SIZE)

    # 3. Normalisation
    if NORMALIZE:
        image = normalize_image(image)

    # 4. Conversion couleur
    if COLOR_MODE == "RGB":
        image = convert_bgr_to_rgb(image)

    return image, original_shape


def preprocess_batch(image_inputs: list) -> list:
    """
    Applique le pipeline de prétraitement à une liste d'images.

    Utile pour les évaluations en batch.
    """
    results = []
    for inp in image_inputs:
        preprocessed, shape = preprocess(inp)
        results.append((preprocessed, shape))
    return results
