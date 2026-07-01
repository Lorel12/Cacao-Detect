"""
data_preparation.py
-------------------
Prépare le dataset pour l'entraînement YOLOv8.

Deux sources sont supportées :
  1. Roboflow  : téléchargement direct via l'API (recommandé)
  2. Local     : organisation d'images brutes déjà disponibles

Exécution :
    python data_preparation.py --source roboflow
    python data_preparation.py --source local --input /chemin/vers/images
"""

import os
import shutil
import argparse
import yaml
from pathlib import Path
from sklearn.model_selection import train_test_split

from config import (
    DATASET_DIR, CLASS_NAMES, NUM_CLASSES, DATASET_YAML
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def create_directory_structure():
    """Crée l'arborescence train/val/test attendue par YOLOv8."""
    for split in ["train", "val", "test"]:
        for sub in ["images", "labels"]:
            path = DATASET_DIR / split / sub
            path.mkdir(parents=True, exist_ok=True)
    print("[✓] Arborescence du dataset créée.")


def generate_dataset_yaml():
    """
    Génère le fichier dataset.yaml requis par YOLOv8
    pour localiser les données et les noms de classes.
    """
    config = {
        "path"  : str(DATASET_DIR),
        "train" : "train/images",
        "val"   : "val/images",
        "test"  : "test/images",
        "nc"    : NUM_CLASSES,
        "names" : CLASS_NAMES,
    }
    with open(DATASET_YAML, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    print(f"[✓] dataset.yaml généré : {DATASET_YAML}")


# ── Source 1 : Roboflow ───────────────────────────────────────────────────────

def download_from_roboflow(api_key: str, workspace: str,
                            project: str, version: int):
    """
    Télécharge un dataset annoté depuis Roboflow.

    Prérequis : pip install roboflow

    Paramètres (à renseigner dans les variables d'environnement
    ou passer en arguments CLI) :
        api_key   : clé API Roboflow
        workspace : slug du workspace Roboflow
        project   : slug du projet Roboflow
        version   : numéro de version du dataset
    """
    try:
        from roboflow import Roboflow
    except ImportError:
        raise ImportError(
            "Installez le SDK Roboflow : pip install roboflow"
        )

    rf = Roboflow(api_key=api_key)
    project_rf = rf.workspace(workspace).project(project)
    dataset = project_rf.version(version).download(
        "yolov5pytorch",
        location=str(DATASET_DIR)
    )
    print(f"[✓] Dataset téléchargé depuis Roboflow → {DATASET_DIR}")
    return dataset


# ── Source 2 : Images locales ─────────────────────────────────────────────────

def prepare_from_local(input_dir: str,
                        val_ratio: float = 0.15,
                        test_ratio: float = 0.10):
    """
    Organise des images brutes déjà annotées (format YOLO) depuis
    un dossier local vers la structure train/val/test.

    Structure attendue en entrée :
        input_dir/
            images/  ← fichiers .jpg / .png
            labels/  ← fichiers .txt (annotations YOLO)

    Les fichiers sont répartis aléatoirement selon les ratios fournis.
    """
    input_dir = Path(input_dir)
    images_dir = input_dir / "images"
    labels_dir = input_dir / "labels"

    if not images_dir.exists():
        raise FileNotFoundError(f"Dossier images introuvable : {images_dir}")
    if not labels_dir.exists():
        raise FileNotFoundError(f"Dossier labels introuvable : {labels_dir}")

    # Récupère les images ayant un label correspondant
    image_files = sorted([
        f for f in images_dir.iterdir()
        if f.suffix.lower() in {".jpg", ".jpeg", ".png"}
        and (labels_dir / f.with_suffix(".txt").name).exists()
    ])

    if not image_files:
        raise ValueError("Aucune paire image/label trouvée dans le dossier source.")

    print(f"[i] {len(image_files)} paires image/label trouvées.")

    # Découpage train / val / test
    train_files, temp_files = train_test_split(
        image_files, test_size=(val_ratio + test_ratio), random_state=42
    )
    relative_test = test_ratio / (val_ratio + test_ratio)
    val_files, test_files = train_test_split(
        temp_files, test_size=relative_test, random_state=42
    )

    splits = {
        "train": train_files,
        "val"  : val_files,
        "test" : test_files,
    }

    for split_name, files in splits.items():
        for img_path in files:
            lbl_path = labels_dir / img_path.with_suffix(".txt").name

            shutil.copy2(img_path, DATASET_DIR / split_name / "images" / img_path.name)
            shutil.copy2(lbl_path, DATASET_DIR / split_name / "labels" / lbl_path.name)

        print(f"[✓] {split_name:5s} : {len(files)} images copiées.")


# ── Statistiques du dataset ───────────────────────────────────────────────────

def print_dataset_stats():
    """Affiche le nombre d'images par split."""
    print("\n── Statistiques du dataset ──────────────────────")
    total = 0
    for split in ["train", "val", "test"]:
        images = list((DATASET_DIR / split / "images").glob("*"))
        count = len(images)
        total += count
        print(f"  {split:5s} : {count:4d} images")
    print(f"  {'TOTAL':5s} : {total:4d} images")
    print("─────────────────────────────────────────────────\n")


# ── Point d'entrée ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Préparation du dataset CacaoDetect pour YOLOv8"
    )
    parser.add_argument(
        "--source", choices=["roboflow", "local"], required=True,
        help="Source des données : 'roboflow' ou 'local'"
    )
    parser.add_argument(
        "--input", type=str, default=None,
        help="(Source 'local') Chemin du dossier contenant images/ et labels/"
    )
    parser.add_argument(
        "--api-key", type=str, default=os.getenv("ROBOFLOW_API_KEY"),
        help="(Source 'roboflow') Clé API Roboflow"
    )
    parser.add_argument(
        "--workspace", type=str, default=os.getenv("ROBOFLOW_WORKSPACE"),
        help="(Source 'roboflow') Workspace slug"
    )
    parser.add_argument(
        "--project", type=str, default=os.getenv("ROBOFLOW_PROJECT"),
        help="(Source 'roboflow') Project slug"
    )
    parser.add_argument(
        "--version", type=int, default=1,
        help="(Source 'roboflow') Numéro de version du dataset"
    )
    args = parser.parse_args()

    create_directory_structure()

    if args.source == "roboflow":
        if not args.api_key:
            raise ValueError(
                "Clé API Roboflow requise (--api-key ou ROBOFLOW_API_KEY)."
            )
        download_from_roboflow(
            api_key=args.api_key,
            workspace=args.workspace,
            project=args.project,
            version=args.version,
        )
    elif args.source == "local":
        if not args.input:
            raise ValueError(
                "Chemin du dossier source requis (--input)."
            )
        prepare_from_local(args.input)

    generate_dataset_yaml()
    print_dataset_stats()


if __name__ == "__main__":
    main()
