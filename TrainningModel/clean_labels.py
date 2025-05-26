import os

LABEL_DIR = "../coco_domestic/labels/train"
MAX_CLASS = 16

for fname in os.listdir(LABEL_DIR):
    if not fname.endswith(".txt"):
        continue
    path = os.path.join(LABEL_DIR, fname)
    with open(path) as f:
        for line in f:
            cls_id = int(line.strip().split()[0])
            if cls_id > MAX_CLASS:
                print(f"{fname} has class ID {cls_id}")
