import json
import os
import math
from pathlib import Path
from PIL import Image

GALLERY_PATH = "galerie"
EXTENSIONS = {".jpg", ".jpeg", ".png"}
OUTPUT = "dirmap.json"

def scan_for_files(path):
    files = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and os.path.splitext(item)[1].lower() in EXTENSIONS:
            files.append(item)
            #print("nalezen soubor: " + item_path)
    return files

def get_txt(path):
    # only one txt is expected per folder, so the program will grab the first one and return.
    for item in os.listdir(path):
        txt_path = os.path.join(path, item)
        if os.path.isfile(txt_path) and os.path.splitext(item)[1].lower() == ".txt":
            print("Nalezen textový soubor " + txt_path)
            with open(txt_path, "r", encoding="utf-8") as f:
                lines = [
                    line.strip()
                    for line in f.read().splitlines()
                    if line.strip()
                ]
            return lines

# go through any folders recursively
def folder_scan(path, is_gallery): # is_gallery is currently redundant, should change json structure based on folder type if needed
    subfolders = {}
    folder_items = {}
    folder_contents = {}
    rescan_needed = False

    print("Procházím složku " + path)
    folder_items = scan_for_files(path) # get all items in this section/folder
    txt_lines = get_txt(path) # get the text file

    # do the same for each subfolder in the parent folder
    for subfolder in os.listdir(path):
        subfolder_path = os.path.join(path, subfolder)
        if os.path.isdir(subfolder_path):
            print("Nalezena podsložka " + subfolder_path)
            subfolders[subfolder] = folder_scan(subfolder_path, is_gallery)

    if folder_items:
        folder_contents["items"] = folder_items
        if is_gallery:
            rescan_needed = image_process(path)
            print(f"rescan_needed: {rescan_needed}")
        
    for name, data in subfolders.items(): # flatten subfolder entries directly into parent
        folder_contents[name] = data

    if txt_lines: # remove this if we want to have txt=NULL in the json for easier later processing
        folder_contents["text"] = txt_lines

    if rescan_needed:
        print(f"Znovuskenuji slozku {path}")
        folder_contents = folder_scan(path, is_gallery) # if there were any processing changes, rescan the folder to make dirmap contain also the processed files
    
    print("\n")

    return folder_contents

def gallery_scan():
    sections = {}
    section_items = {}
    subfolders = {}

    # Loop over each section (doplnky, reference, stoly) in GALLERY_PATH
    for section in os.listdir(GALLERY_PATH):
        section_path = os.path.join(GALLERY_PATH, section)
        if os.path.isdir(section_path):
            print("\n\nProcházím sekci " + section + "\n")

            if section == "stoly" or section == "doplnky":
                sections[section] = folder_scan(section_path, True)
            else: 
                sections[section] = folder_scan(section_path, False)
            
            # Use the section name as the key
    return sections

def needs_update(src, dst):
    if not os.path.exists(dst):
        return True
    return os.path.getmtime(src) > os.path.getmtime(dst) 

def get_dims(path):
    print(path)
    max_w = 0
    max_h = 0
    min_w = math.inf
    min_h = math.inf

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and os.path.splitext(item)[1].lower() in EXTENSIONS:
            with Image.open(item_path) as im:
                max_w = max(max_w, im.width)
                max_h = max(max_h, im.height)
                min_w = min(min_w, im.width)
                min_h = min(min_h, im.height)

    return {
        "min_w": min_w,
        "min_h": min_h,
        "max_w": max_w,
        "max_h": max_h,
    }

def scale_and_compress(src, dst, size):
    # create parent directories if they don't exist
    output_path = Path(dst)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # TODO, cap img px size to like 2000, scale if bigger.
    with Image.open(src) as im:
        im = im.convert("RGB")

        canvas = Image.new("RGB", size, (0,0,0))

        x = (size[0] - im.width)//2
        y = (size[1] - im.height)//2

        print(f"Ukládám obr. {output_path}")
        canvas.paste(im, (x,y))
        canvas.save(output_path, "JPEG",
            quality=85,
            optimize=True,
            progressive=True
        )

def make_thumbnail(src, dst):
    # create parent directories if they don't exist
    output_path = Path(dst)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im.thumbnail((300,300))
        im.save(output_path, "JPEG", quality=70, optimize=True)

def image_process(folder_path): #called per folder
    processed_something = False
    gallery_dims = {}
    
    if "processed" in Path(folder_path).parts or "thumbnails" in Path(folder_path).parts:
        return processed_something

    print("Processing: " + folder_path)

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        processed_item_path = os.path.join(folder_path, "processed", item)
        thumbnail_path = os.path.join(folder_path, "thumbnails", item)

        if not (os.path.isfile(item_path) and os.path.splitext(item)[1].lower() in EXTENSIONS):
            continue
        
        print("kontroluji obrázek " + item_path)

        # process images (downscaling, borders)
        if needs_update(item_path, processed_item_path):
            processed_something = True
            # set all images to the minimum present height, then pad the width, then compress
            print(f"obr. je nutno aktualizovat!")
            if not gallery_dims:
                gallery_dims = get_dims(folder_path)
                print(gallery_dims)
            
            scale_and_compress(item_path, processed_item_path, (gallery_dims["max_w"], gallery_dims["min_h"]))
        
        # create thumbnails
        if needs_update(item_path, thumbnail_path):
            processed_something = True
            # set all images to the minimum present height, then pad the width, then compress
            print(f"miniaturu obr. je nutno aktualizovat!")
            make_thumbnail(item_path, thumbnail_path)

    return processed_something


def save_json(map, file):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(map, f, indent=4)
    print("===============================\nMapa adresáře byla úspěšně aktualizována!\n===============================") 

if __name__ == "__main__":
    file_map = gallery_scan()
    save_json(file_map, OUTPUT)
