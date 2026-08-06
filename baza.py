import json
import os
import datetime
import shutil
from generuj_pdf import generujPdf

FOLDER_PROJEKTU = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(FOLDER_PROJEKTU, "reklamacje.json")
FOLDER_DANYCH = os.path.join(FOLDER_PROJEKTU, "Reklamacje_Dane")


def wczytajDane():
    if not os.path.exists(DATABASE):
        return []

    with open(DATABASE, "r", encoding="utf-8") as f:
        try: 
            return json.load(f)
        except json.JSONDecodeError:
            return []


def zapiszReklamacje(dane):
    with open(DATABASE, "w", encoding="utf-8") as f:
        json.dump(dane, f, indent=2, ensure_ascii=False)



def przygotuj_i_kopiuj_zalaczniki(
    rok, id_zgl, nr_rek, lista_sciezek_zrodlowych, dane
):

    if not lista_sciezek_zrodlowych:
        lista_sciezek_zrodlowych = []

    nazwa_folderu = nr_rek.replace("/", "_")
    folder_docelowy = os.path.join(FOLDER_DANYCH, nazwa_folderu)
    os.makedirs(folder_docelowy, exist_ok=True)

    zapisane_pliki = []

    try:
        sciezka_pdf = generujPdf(
            folder_docelowy, dane, nr_rek, FOLDER_PROJEKTU
        )
        zapisane_pliki.append(sciezka_pdf)
    except Exception as e:
        print(f"[BŁĄD GENEROWANIA PDF]: {e}")

    for sciezka_pliku in lista_sciezek_zrodlowych:
        if os.path.exists(sciezka_pliku):
            nazwa_pliku = os.path.basename(sciezka_pliku)
            sciezka_docelowa = os.path.join(folder_docelowy, nazwa_pliku)

            shutil.copy2(sciezka_pliku, sciezka_docelowa)
            sciezka_wzgledna = os.path.relpath(
                sciezka_docelowa, FOLDER_PROJEKTU
            )
            zapisane_pliki.append(sciezka_wzgledna)

    return zapisane_pliki


def dodajReklamacje(nowe_zgloszenie, lista_zalacznikow_sciezki):
    reklamacje = wczytajDane()

    max_id = max([r.get("id", 0) for r in reklamacje], default=0)
    nowe_id = max_id + 1
    rok = datetime.date.today().year
    nr_rek = f"ZG/{rok}/{nowe_id:03d}"

    sciezki_zalacznikow = przygotuj_i_kopiuj_zalaczniki(
        rok, nowe_id, nr_rek, lista_zalacznikow_sciezki, nowe_zgloszenie
    )

    nowe_zgloszenie["id"] = nowe_id
    nowe_zgloszenie["nr_rek"] = nr_rek
    nowe_zgloszenie["zalaczniki"] = sciezki_zalacznikow

    reklamacje.append(nowe_zgloszenie)
    zapiszReklamacje(reklamacje)