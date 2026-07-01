"""
config.py
---------
Paramètres centralisés du module IA de CacaoDetect.
Toutes les constantes sont définies ici pour éviter
les valeurs « magiques » dispersées dans le code.
"""

import os
from pathlib import Path

# ── Chemins ───────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
DATASET_DIR = BASE_DIR / "dataset"

# Chemin vers les poids du modèle actif
MODEL_PATH = MODELS_DIR / "cacaodetect_yolov8n.pt"

# Fichier de configuration YAML du dataset (généré par data_preparation.py)
DATASET_YAML = DATASET_DIR / "dataset.yaml"

# ── Classes ───────────────────────────────────────────────────────────────────
# 6 classes : 5 maladies + 1 état sain
CLASS_NAMES = [
    "sain",
    "pourriture_brune",       # Phytophthora palmivora
    "moniliophthora",         # Moniliophthora roreri
    "anthracnose",            # Colletotrichum gloeosporioides
    "cochenilles",            # Pseudococcidae
    "balai_de_sorciere",      # Moniliophthora perniciosa
]
NUM_CLASSES = len(CLASS_NAMES)

# ── Prétraitement ─────────────────────────────────────────────────────────────
IMG_SIZE   = 640          # Taille d'entrée du modèle (640×640 px)
NORMALIZE  = True         # Normalisation [0, 1]
COLOR_MODE = "RGB"        # Conversion BGR→RGB (OpenCV lit en BGR par défaut)

# ── Inférence ─────────────────────────────────────────────────────────────────
CONF_THRESHOLD = 0.45     # Seuil de confiance minimum
IOU_THRESHOLD  = 0.50     # Seuil IoU pour la suppression non-maximale (NMS)
MAX_DETECTIONS = 10       # Nombre maximum de détections par image
INFERENCE_TIMEOUT_S = 10  # Délai maximum d'inférence en secondes
MAX_RETRIES = 2           # Nombre de tentatives en cas d'échec

# ── Niveaux de gravité ────────────────────────────────────────────────────────
# Basés sur le ratio : surface détectée / surface totale de l'image
GRAVITY_THRESHOLDS = {
    "faible":  0.15,   # < 15 %  → surveillance, traitement préventif
    "modere":  0.40,   # 15–40 % → traitement curatif localisé
    "eleve":   1.00,   # > 40 %  → traitement intensif, alerte agronomique
}

# ── Entraînement ──────────────────────────────────────────────────────────────
TRAIN_CONFIG = {
    "model"      : "yolov8n.pt",   # Poids de base pré-entraînés (COCO)
    "epochs"     : 10,
    "patience"   : 20,             # Early stopping
    "batch"      : 16,
    "imgsz"      : IMG_SIZE,
    "optimizer"  : "SGD",
    "lr0"        : 0.01,           # Learning rate initial
    "momentum"   : 0.937,
    "weight_decay": 0.0005,
    "project"    : str(MODELS_DIR / "runs"),
    "name"       : "cacaodetect_v1",
    "exist_ok"   : True,
    # Augmentation
    "fliplr"     : 0.5,
    "flipud"     : 0.5,
    "degrees"    : 15.0,           # Rotation ±15°
    "hsv_v"      : 0.4,            # Variation de luminosité ±40 %
    "translate"  : 0.1,
    "scale"      : 0.5,
    "mosaic"     : 1.0,
}

# ── Annotation visuelle ───────────────────────────────────────────────────────
ANNOTATION_COLORS = {
    "sain"             : (0, 200, 0),      # Vert
    "pourriture_brune" : (0, 60, 200),     # Marron-bleu
    "moniliophthora"   : (0, 140, 255),    # Orange
    "anthracnose"      : (0, 0, 220),      # Rouge
    "cochenilles"      : (180, 0, 180),    # Violet
    "balai_de_sorciere": (0, 200, 200),    # Cyan
}
BOX_THICKNESS  = 2
FONT_SCALE     = 0.6
LABEL_PADDING  = 5

# ── Stockage (AWS S3) ─────────────────────────────────────────────────────────
S3_BUCKET          = os.getenv("S3_BUCKET", "cacaodetect-storage")
S3_PREFIX_ANNOTATED = "analyses/annotated/"
S3_PREFIX_RAW       = "analyses/raw/"
