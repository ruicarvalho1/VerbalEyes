import os
import shutil
import random

# === CONFIG ===
src_img_dir = "../coco_domestic/images/train"
src_lbl_dir = "../coco_domestic/labels/train"
dst_val_img = "../coco_domestic/images/val"
dst_val_lbl = "../coco_domestic/labels/val"

COCO_TO_NEW = {
    62: 0, 69: 1, 70: 2, 72: 3, 81: 4, 78: 5,
    59: 6, 57: 7, 60: 8, 63: 9, 67: 10, 73: 11,
    75: 12, 77: 13, 84: 14, 74: 15, 47: 16
}

MAX_NEW_ID = max(COCO_TO_NEW.values())

os.makedirs(dst_val_img, exist_ok=True)
os.makedirs(dst_val_lbl, exist_ok=True)

print("Reindexing class IDs in labels...")
for file in os.listdir(src_lbl_dir):
    if not file.endswith(".txt"):
        continue
    path = os.path.join(src_lbl_dir, file)
    lines_fixed = []
    with open(path) as f:
        for line in f:
            parts = line.strip().split()
            cls = int(parts[0])
            if cls in COCO_TO_NEW:
                new_cls = COCO_TO_NEW[cls]
                lines_fixed.append(f"{new_cls} {' '.join(parts[1:])}")
            else:

                continue
    with open(path, "w") as f:
        f.write("\n".join(lines_fixed))


img_files = [f for f in os.listdir(src_img_dir) if f.endswith(".jpg")]
val_sample = random.sample(img_files, int(len(img_files) * 0.1))

for fname in val_sample:
    label_name = fname.replace(".jpg", ".txt")
    shutil.move(os.path.join(src_img_dir, fname), os.path.join(dst_val_img, fname))
    shutil.move(os.path.join(src_lbl_dir, label_name), os.path.join(dst_val_lbl, label_name))

print(f"Moved {len(val_sample)} images and labels to validation set.")
