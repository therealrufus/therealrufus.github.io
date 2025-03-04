import json
import os

GALLERY_PATH = "galerie"
EXTENSIONS = {".jpg", ".jpeg", ".png"}
OUTPUT = "dirmap.json"

def folder_scan(path):
    items = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and os.path.splitext(item)[1].lower() in EXTENSIONS:
            items.append(item)
    return items

def gallery_scan():
    directories = {}

    # Loop over each section (gallery) in GALLERY_PATH
    for section in os.listdir(GALLERY_PATH):
        section_path = os.path.join(GALLERY_PATH, section)
        if os.path.isdir(section_path):
            folder_items = folder_scan(section_path)

            subfolders = {}
            for item in os.listdir(section_path):
                item_path = os.path.join(section_path, item)
                if os.path.isdir(item_path):
                    sub_items = folder_scan(item_path)
                    if sub_items:
                        subfolders[item] = sub_items

            # Use the section name as the key
            directories[section] = {
                "items": folder_items,
                "subfolders": subfolders
            }
    return directories

def save_json(map, file):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(map, f, indent=4)
    print("===============================\nMapa adresáře byla úspěšně aktualizována!\n===============================") 

if __name__ == "__main__":
    file_map = gallery_scan()
    save_json(file_map, OUTPUT)
