import json
import os

GALLERY_PATH = "galerie"
EXTENSIONS = {".jpg", ".jpeg", ".png"}
OUTPUT = "dirmap.json"

def scan_for_files(path):
    files = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and os.path.splitext(item)[1].lower() in EXTENSIONS:
            files.append(item)
            print("nalezen soubor: " + item_path)
    return files

def get_txt(path):
    #only one txt is expected per folder, so the program will grab the first one and return.
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
def folder_scan(path, is_gallery):
    subfolders = {}
    folder_items = {}
    folder_contents = {}

    print("Procházím složku " + path)
    folder_items = scan_for_files(path) # get all items in this section/folder
    txt_lines = get_txt(path) # get the text file

    # do the same for each subfolder in the parent folder
    for subfolder in os.listdir(path):
        subfolder_path = os.path.join(path, subfolder)
        if os.path.isdir(subfolder_path):
            print("Nalezena podsložka " + subfolder_path)
            subfolders[subfolder] = folder_scan(subfolder_path)

    if folder_items:
        folder_contents["items"] = folder_items
        
    for name, data in subfolders.items(): # flatten subfolder entries directly into parent
        folder_contents[name] = data

    folder_contents["text"] = txt_lines
    print("\n")

    return folder_contents
    
def image_process(path):
    return

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

def save_json(map, file):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(map, f, indent=4)
    print("===============================\nMapa adresáře byla úspěšně aktualizována!\n===============================") 

if __name__ == "__main__":
    file_map = gallery_scan()
    save_json(file_map, OUTPUT)
