"""
evaluate.py
-----------
Évalue les performances du modèle YOLOv8 entraîné
sur le jeu de données de test.

Métriques calculées :
  - mAP@0.50    : mean Average Precision au seuil IoU 0.50
  - mAP@0.50:0.95 : mAP moyen sur plusieurs seuils IoU
  - Précision   : taux de vrais positifs parmi les détections
  - Rappel      : taux de vrais positifs parmi les cas réels

Exécution :
    python evaluate.py
    python evaluate.py --model /chemin/vers/autre_modele.pt
"""

import argparse
from pathlib import Path
from ultralytics import YOLO

from config import MODEL_PATH, DATASET_YAML, CLASS_NAMES, CONF_THRESHOLD, IOU_THRESHOLD


def evaluate(model_path: Path = MODEL_PATH,
             split: str = "test") -> dict:
    """
    Évalue le modèle sur un split du dataset.

    Paramètres :
        model_path : chemin vers les poids .pt à évaluer
        split      : "val" ou "test"

    Retourne :
        dict avec les métriques principales.
    """
    if not model_path.exists():
        raise FileNotFoundError(
            f"Modèle introuvable : {model_path}\n"
            "Lancez d'abord train.py pour entraîner le modèle."
        )
    if not DATASET_YAML.exists():
        raise FileNotFoundError(
            f"dataset.yaml introuvable : {DATASET_YAML}"
        )

    print(f"\n── Évaluation du modèle ──────────────────────────────────")
    print(f"  Modèle  : {model_path}")
    print(f"  Dataset : {DATASET_YAML}")
    print(f"  Split   : {split}")
    print(f"  Conf    : {CONF_THRESHOLD}  |  IoU : {IOU_THRESHOLD}")
    print("─────────────────────────────────────────────────────────\n")

    model = YOLO(str(model_path))

    metrics = model.val(
        data=str(DATASET_YAML),
        split=split,
        conf=CONF_THRESHOLD,
        iou=IOU_THRESHOLD,
        verbose=True,
    )

    # Extraction des métriques clés
    results = {
        "mAP50"      : round(float(metrics.box.map50), 4),
        "mAP50_95"   : round(float(metrics.box.map), 4),
        "precision"  : round(float(metrics.box.mp), 4),
        "recall"     : round(float(metrics.box.mr), 4),
        "per_class"  : {},
    }

    # Métriques par classe
    if hasattr(metrics.box, "ap_class_index"):
        for i, class_idx in enumerate(metrics.box.ap_class_index):
            class_name = CLASS_NAMES[class_idx] if class_idx < len(CLASS_NAMES) else f"class_{class_idx}"
            results["per_class"][class_name] = {
                "AP50"     : round(float(metrics.box.ap50[i]), 4),
                "precision": round(float(metrics.box.p[i]), 4),
                "recall"   : round(float(metrics.box.r[i]), 4),
            }

    # Affichage formaté
    print("\n── Résultats ─────────────────────────────────────────────")
    print(f"  mAP@0.50       : {results['mAP50']:.4f}")
    print(f"  mAP@0.50:0.95  : {results['mAP50_95']:.4f}")
    print(f"  Précision      : {results['precision']:.4f}")
    print(f"  Rappel         : {results['recall']:.4f}")
    if results["per_class"]:
        print("\n  Par classe :")
        for cls, m in results["per_class"].items():
            print(f"    {cls:25s} | AP50: {m['AP50']:.4f} | P: {m['precision']:.4f} | R: {m['recall']:.4f}")
    print("─────────────────────────────────────────────────────────\n")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Évaluation du modèle CacaoDetect"
    )
    parser.add_argument(
        "--model", type=str, default=str(MODEL_PATH),
        help="Chemin vers les poids .pt à évaluer"
    )
    parser.add_argument(
        "--split", choices=["val", "test"], default="test",
        help="Split du dataset à utiliser (défaut : test)"
    )
    args = parser.parse_args()
    evaluate(model_path=Path(args.model), split=args.split)


if __name__ == "__main__":
    main()
