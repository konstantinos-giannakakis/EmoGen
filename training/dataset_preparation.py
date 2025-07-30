import json
import os
import shutil
from tqdm import tqdm

# EmoSet118Kを"object","scene"に分類

root_annotation = "/mnt/c/Users/giann/Downloads/EmoSet-118K/annotation"
root_image = "/mnt/c/Users/giann/Downloads/EmoSet-118K/image"
root_new = "/mnt/c/Users/giann/Downloads/EmoSet-118K_organized"


# Collect all annotation files first for progress bar
annotation_files = []
for curDir, _, files in os.walk(root_annotation):
    for file in files:
        if file.endswith("json"):
            annotation_files.append((curDir, file))

for curDir, file in tqdm(annotation_files, desc="Processing annotations"):
    # load json file
    json_file_path = os.path.join(curDir, file)
    with open(json_file_path, "r") as f:
        data = json.load(f)

    image_value = data["image_id"]
    emotion_value = data["emotion"]

    if "object" in data:
        object_values = data.get("object", [])
        for object_value in object_values:
            # make object dir
            object_dir = os.path.join(root_new, "object", object_value)
            os.makedirs(object_dir, exist_ok=True)

            # create symlink to image in object dir
            image_dir = os.path.join(root_image, emotion_value, image_value + ".jpg")
            symlink_path = os.path.join(object_dir, os.path.basename(image_dir))
            try:
                os.symlink(image_dir, symlink_path)
            except FileExistsError:
                pass

    if "scene" in data:
        # make scene dir
        scene_value = data["scene"]
        scene_dir = os.path.join(root_new, "scene", scene_value)
        os.makedirs(scene_dir, exist_ok=True)

        # create symlink to image in scene dir
        image_dir = os.path.join(root_image, emotion_value, image_value + ".jpg")
        symlink_path = os.path.join(scene_dir, os.path.basename(image_dir))
        try:
            os.symlink(image_dir, symlink_path)
        except FileExistsError:
            pass
