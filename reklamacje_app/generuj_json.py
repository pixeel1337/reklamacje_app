import json 
import os

def generujJSON(folder_docelowy, dane, nazwa_folderu, folder_projektu):
    nazwa_json = f"{nazwa_folderu}.json"
    sciezka_json = os.path.join(folder_docelowy, nazwa_json)

    with open(sciezka_json, "w", encoding="utf-8") as f:
        json.dump(dane, f, indent=2, ensure_ascii=False)

    return os.path.relpath(sciezka_json, folder_projektu)

