import os
from urllib.request import urlretrieve
import zipfile

def download_and_extract(url, dest_folder):
    filename = url.split("/")[-1]
    zip_path = os.path.join(dest_folder, filename)
    print(f"Downloading {filename}...")
    urlretrieve(url, zip_path)
    print("Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)
    os.remove(zip_path)
    print("Completed:", filename)

base_dir = "./coco"
os.makedirs(base_dir, exist_ok=True)


download_and_extract("http://images.cocodataset.org/zips/train2017.zip", base_dir)
download_and_extract("http://images.cocodataset.org/zips/val2017.zip", base_dir)
download_and_extract("http://images.cocodataset.org/annotations/annotations_trainval2017.zip", base_dir)
