"""
inference.py
------------
Chargement du modèle YOLOv8 et exécution de l'inférence.

Principes (conformes au cahier de conception) :
  - Singleton : le modèle est chargé une seule fois en mémoire
    au démarrage du serveur pour éviter les rechargements coûteux.
  - Timeout : 10 secondes maximum par requête d'inférence.
  - Retries : 2 tentatives automatiques avant retour d'erreur.
"""

import time
import threading
import numpy as np
from pathlib import Path
from typing import Optional
from ultralytics import YOLO

from config import (
    MODEL_PATH, CONF_THRESHOLD, IOU_THRESHOLD,
    MAX_DETECTIONS, INFERENCE_TIMEOUT_S, MAX_RETRIES, CLASS_NAMES
)


# ── Singleton du modèle ───────────────────────────────────────────────────────

class ModelSingleton:
    """
    Gestionnaire du modèle YOLOv8 en tant que singleton thread-safe.

    Garantit qu'une seule instance du modèle existe en mémoire,
    quel que soit le nombre de requêtes simultanées.
    """
    _instance: Optional["ModelSingleton"] = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._model = None
        return cls._instance

    def load(self, model_path: Path = MODEL_PATH) -> None:
        """Charge le modèle depuis le disque. Appelé une seule fois au démarrage."""
        if self._model is not None:
            return  # Déjà chargé

        if not model_path.exists():
            raise FileNotFoundError(
                f"Fichier de poids introuvable : {model_path}\n"
                "Lancez d'abord train.py pour entraîner le modèle."
            )
        print(f"[IA] Chargement du modèle : {model_path}")
        self._model = YOLO(str(model_path))
        print("[IA] Modèle chargé en mémoire.")

    @property
    def model(self) -> YOLO:
        if self._model is None:
            raise RuntimeError(
                "Le modèle n'est pas encore chargé. "
                "Appelez ModelSingleton().load() au démarrage."
            )
        return self._model


# Instance globale (importée par ia_service.py)
model_singleton = ModelSingleton()


# ── Inférence ─────────────────────────────────────────────────────────────────

def _run_inference(image: np.ndarray) -> list:
    """
    Exécute l'inférence YOLOv8 sur une image prétraitée.

    Paramètre :
        image : np.ndarray (640×640, float32, RGB) — sortie de preprocessing.py

    Retourne :
        Liste des détections brutes de l'objet Results d'Ultralytics.
    """
    results = model_singleton.model.predict(
        source=image,
        conf=CONF_THRESHOLD,
        iou=IOU_THRESHOLD,
        max_det=MAX_DETECTIONS,
        verbose=False,
    )
    return results


def run_inference_with_timeout(image: np.ndarray) -> list:
    """
    Lance l'inférence avec timeout et système de retries.

    Conforme au cahier de conception :
      - Délai max : INFERENCE_TIMEOUT_S secondes (10 s)
      - Tentatives : MAX_RETRIES (2) avant retour d'erreur

    Retourne :
        Liste des objets Results d'Ultralytics.

    Lève :
        TimeoutError  : si toutes les tentatives dépassent le timeout.
        RuntimeError  : si une erreur interne survient après tous les retries.
    """
    last_error = None

    for attempt in range(1, MAX_RETRIES + 2):  # MAX_RETRIES + 1 tentative initiale
        result_holder = []
        error_holder  = []

        def target():
            try:
                result_holder.extend(_run_inference(image))
            except Exception as e:
                error_holder.append(e)

        thread = threading.Thread(target=target, daemon=True)
        start  = time.time()
        thread.start()
        thread.join(timeout=INFERENCE_TIMEOUT_S)
        elapsed = time.time() - start

        if thread.is_alive():
            last_error = TimeoutError(
                f"Tentative {attempt} : timeout dépassé ({elapsed:.1f}s > {INFERENCE_TIMEOUT_S}s)."
            )
            print(f"[IA] {last_error}")
            continue

        if error_holder:
            last_error = error_holder[0]
            print(f"[IA] Tentative {attempt} échouée : {last_error}")
            continue

        return result_holder  # Succès

    raise last_error or RuntimeError("Échec de l'inférence après toutes les tentatives.")


# ── Parsing des résultats ──────────────────────────────────────────────────────

def parse_results(results: list, original_shape: tuple) -> list:
    """
    Convertit les objets Results d'Ultralytics en liste de dictionnaires
    normalisés, prêts à être consommés par postprocessing.py.

    Paramètres :
        results        : sortie de run_inference_with_timeout()
        original_shape : (hauteur, largeur) de l'image AVANT redimensionnement

    Retourne :
        Liste de dicts avec les clés :
            class_id    (int)   : identifiant de la classe prédite
            class_name  (str)   : nom lisible de la classe
            confidence  (float) : score de confiance [0, 1]
            bbox        (dict)  : boîte englobante en pixels de l'image originale
                                  {x1, y1, x2, y2, width, height}
    """
    detections = []
    orig_h, orig_w = original_shape

    for result in results:
        boxes = result.boxes
        if boxes is None or len(boxes) == 0:
            continue

        for box in boxes:
            # Coordonnées en pixels dans l'espace 640×640
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf  = float(box.conf[0])
            cls_id = int(box.cls[0])

            # Mise à l'échelle vers les dimensions originales
            scale_x = orig_w / 640
            scale_y = orig_h / 640
            x1_orig = x1 * scale_x
            y1_orig = y1 * scale_y
            x2_orig = x2 * scale_x
            y2_orig = y2 * scale_y

            detections.append({
                "class_id"   : cls_id,
                "class_name" : CLASS_NAMES[cls_id] if cls_id < len(CLASS_NAMES) else "inconnu",
                "confidence" : round(conf, 4),
                "bbox"       : {
                    "x1"    : round(x1_orig),
                    "y1"    : round(y1_orig),
                    "x2"    : round(x2_orig),
                    "y2"    : round(y2_orig),
                    "width" : round(x2_orig - x1_orig),
                    "height": round(y2_orig - y1_orig),
                },
            })

    # Tri par score de confiance décroissant
    detections.sort(key=lambda d: d["confidence"], reverse=True)
    return detections
