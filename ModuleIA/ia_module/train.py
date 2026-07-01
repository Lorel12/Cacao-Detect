"""
train.py
--------
Entraînement du modèle YOLOv8n sur le dataset de maladies du cacaoyer.

Paramètres d'entraînement conformes au cahier de conception (section VI.1) :
  - Base     : YOLOv8n (pré-entraîné COCO)
  - Epochs   : 150 (early stopping patience = 20)
  - Batch    : 16
  - Imgsz    : 640
  - Optimiseur : SGD, lr=0.01, momentum=0.937
  - Augmentation : flip H/V, rotation ±15°, variation luminosité ±40%

Exécution :
    python train.py
    python train.py --resume   # Reprendre un entraînement interrompu
"""

import argparse
import shutil
from pathlib import Path
from ultralytics import YOLO

from config import (
    DATASET_YAML, MODEL_PATH, MODELS_DIR, TRAIN_CONFIG
)


def check_dataset():
    """Vérifie que le dataset est prêt avant de lancer l'entraînement."""
    if not DATASET_YAML.exists():
        raise FileNotFoundError(
            f"Fichier dataset.yaml introuvable : {DATASET_YAML}\n"
            "Lancez d'abord : python data_preparation.py --source roboflow"
        )
    for split in ["train", "val"]:
        images_dir = DATASET_YAML.parent / split / "images"
        images = list(images_dir.glob("*"))
        if not images:
            raise ValueError(
                f"Aucune image dans le split '{split}' : {images_dir}\n"
                "Vérifiez votre dataset."
            )
        print(f"[✓] {split:5s} : {len(images)} images trouvées.")


def train(resume: bool = False):
    """
    Lance l'entraînement YOLOv8.

    Paramètre :
        resume : si True, reprend depuis le dernier checkpoint.
    """
    check_dataset()

    print("\n── Démarrage de l'entraînement CacaoDetect ──────────────")
    print(f"  Dataset : {DATASET_YAML}")
    print(f"  Epochs  : {TRAIN_CONFIG['epochs']}")
    print(f"  Batch   : {TRAIN_CONFIG['batch']}")
    print(f"  Classes : {TRAIN_CONFIG}")
    print("─────────────────────────────────────────────────────────\n")

    # Chargement du modèle de base pré-entraîné (COCO)
    model = YOLO(TRAIN_CONFIG["model"])

    # Paramètres d'entraînement (issus de config.py)
    train_args = {k: v for k, v in TRAIN_CONFIG.items()}
    train_args["data"] = str(DATASET_YAML)

    if resume:
        # Recherche du dernier checkpoint disponible
        last_ckpt = Path(TRAIN_CONFIG["project"]) / TRAIN_CONFIG["name"] / "weights" / "last.pt"
        if last_ckpt.exists():
            print(f"[i] Reprise depuis : {last_ckpt}")
            train_args["resume"] = True
            model = YOLO(str(last_ckpt))
        else:
            print("[!] Aucun checkpoint trouvé, démarrage depuis zéro.")

    # Entraînement
    results = model.train(**train_args)

    # Copie du meilleur modèle vers models/cacaodetect_yolov8n.pt
    best_weights = (
        Path(TRAIN_CONFIG["project"])
        / TRAIN_CONFIG["name"]
        / "weights"
        / "best.pt"
    )
    if best_weights.exists():
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(best_weights, MODEL_PATH)
        print(f"\n[✓] Meilleur modèle copié → {MODEL_PATH}")
    else:
        print("[!] Fichier best.pt introuvable après entraînement.")

    print("\n[✓] Entraînement terminé.")
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Entraînement YOLOv8 — CacaoDetect"
    )
    parser.add_argument(
        "--resume", action="store_true",
        help="Reprendre depuis le dernier checkpoint"
    )
    args = parser.parse_args()
    train(resume=args.resume)


if __name__ == "__main__":
    main()
