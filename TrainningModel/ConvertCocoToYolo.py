from pycocotools.coco import COCO
import os
from tqdm import tqdm

def convert_coco_to_yolo(json_file, output_dir, image_dir):
    coco = COCO(json_file)
    os.makedirs(output_dir, exist_ok=True)

    image_ids = coco.getImgIds()
    for img_id in tqdm(image_ids):
        img = coco.loadImgs(img_id)[0]
        file_name = img["file_name"]
        w, h = img["width"], img["height"]
        ann_ids = coco.getAnnIds(imgIds=img['id'])
        anns = coco.loadAnns(ann_ids)

        label_file = os.path.join(output_dir, file_name.replace(".jpg", ".txt"))
        with open(label_file, 'w') as f:
            for ann in anns:
                if ann.get("iscrowd", 0):
                    continue
                cat_id = ann['category_id'] - 1
                bbox = ann['bbox']
                x, y, bw, bh = bbox
                xc = (x + bw / 2) / w
                yc = (y + bh / 2) / h
                bw /= w
                bh /= h
                f.write(f"{cat_id} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}\n")

convert_coco_to_yolo(
    json_file='coco/annotations/instances_train2017.json',
    output_dir='coco/labels/train2017',
    image_dir='coco/images/train2017'
)

convert_coco_to_yolo(
    json_file='coco/annotations/instances_val2017.json',
    output_dir='coco/labels/val2017',
    image_dir='coco/images/val2017'
)
