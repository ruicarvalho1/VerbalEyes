import os

def remove_images_without_labels(img_dir, lbl_dir):
    count = 0
    for img in os.listdir(img_dir):
        lbl = img.replace(".jpg", ".txt")
        if not os.path.exists(os.path.join(lbl_dir, lbl)):
            os.remove(os.path.join(img_dir, img))
            count += 1
    print(f"Removed {count} images with no labels from {img_dir}")

remove_images_without_labels("../coco_domestic/images/train", "coco_domestic/labels/train")
remove_images_without_labels("../coco_domestic/images/val", "coco_domestic/labels/val")
