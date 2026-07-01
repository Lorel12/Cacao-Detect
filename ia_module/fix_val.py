import shutil
import random
from pathlib import Path

dataset = Path("dataset")
train_img = dataset / "train" / "images"
train_lbl = dataset / "train" / "labels"
val_img   = dataset / "val"   / "images"
val_lbl   = dataset / "val"   / "labels"

val_img.mkdir(parents=True, exist_ok=True)
val_lbl.mkdir(parents=True, exist_ok=True)

images = list(train_img.glob("*"))
random.seed(42)
val_files = random.sample(images, int(len(images) * 0.15))

for img in val_files:
    lbl = train_lbl / img.with_suffix(".txt").name
    shutil.move(str(img), val_img / img.name)
    if lbl.exists():
        shutil.move(str(lbl), val_lbl / lbl.name)

print(f"Val   : {len(val_files)} images déplacées depuis train")
print(f"Train : {len(list(train_img.glob('*')))} images restantes")
