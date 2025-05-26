import os
import shutil
import json
from tqdm import tqdm


DOMESTIC_CLASSES = [
    'tv', 'microwave', 'oven', 'refrigerator', 'sink', 'toaster',
    'bed', 'couch', 'dining table', 'laptop', 'keyboard', 'mouse',
    'remote', 'cell phone', 'book', 'clock', 'vase'
]


with open("coco.names", "r") as f:
    all_classes = [line.strip() for line in f.readlines()]
coco_id_to_name = {i: name for i, name in enumerate(all_classes)}
selected_ids = [i for i, name in coco_id_to_name.items() if name in DOMESTIC_CLASSES]
id_map = {old_id: new_id for new_id, old_id in enumerate(selected_ids)}


src_img_dir = "coco/train2017"
src_ann_file = "coco/annotations/instances_train2017.json"
dst_img_dir = "../coco_domestic/images/train"
dst_lbl_dir = "../coco_domestic/labels/train"

os.makedirs(dst_img_dir, exist_ok=True)
os.makedirs(dst_lbl_dir, exist_ok=True)


with open(src_ann_file, "r") as f:
    data = json.load(f)

img_id_to_file = {img["id"]: img["file_name"] for img in data["images"]}
annotations_by_img = {}


for ann in data["annotations"]:
    if ann["category_id"] in id_map:
        img_id = ann["image_id"]
        if img_id not in annotations_by_img:
            annotations_by_img[img_id] = []
        annotations_by_img[img_id].append(ann)

print("Copying images and generating YOLO labels...")

for img_id, anns in tqdm(annotations_by_img.items()):
    file_name = img_id_to_file[img_id]
    src_path = os.path.join(src_img_dir, file_name)
    dst_path = os.path.join(dst_img_dir, file_name)
    shutil.copy2(src_path, dst_path)

    width = height = 1
    for img in data["images"]:
        if img["id"] == img_id:
            width = img["width"]
            height = img["height"]
            break

    label_file = os.path.join(dst_lbl_dir, file_name.replace(".jpg", ".txt"))
    with open(label_file, "w") as f:
        for ann in anns:
            x, y, w, h = ann["bbox"]
            cx = (x + w / 2) / width
            cy = (y + h / 2) / height
            nw = w / width
            nh = h / height
            new_id = id_map[ann["category_id"]]
            f.write(f"{new_id} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}\n")

print("Done!")
