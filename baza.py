import datetime
import json
import os
import shutil

from generuj_json import generujJSON
from generuj_pdf import generujPdf

FOLDER_PROJEKTU = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(FOLDER_PROJEKTU, "reklamacje.json")
FOLDER_DANYCH = os.path.join(FOLDER_PROJEKTU, "Reklamacje_Dane")


def wczytajDane():
    """Wczytuje listę wszystkich reklamacji z pliku bazy JSON."""
    if not os.path.exists(DATABASE):
        return []

    with open(DATABASE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def zapiszDane(dane):
    """Zapisuje całą listę reklamacji do pliku bazy JSON."""
    with open(DATABASE, "w", encoding="utf-8") as f:
        json.dump(dane, f, indent=2, ensure_ascii=False)


def pobierzReklamacjePoNumerze(nr_rek):
    """Pomocnicza funkcja: pobiera pojedyncze zgłoszenie na podstawie nr_rek."""
    if not nr_rek:
        return None
    szukany = nr_rek.strip().upper().replace("_", "/")
    for r in wczytajDane():
        if r.get("nr_rek", "").strip().upper().replace("_", "/") == szukany:
            return r
    return None


def aktualizujReklamacje(nr_rek, zaktualizowane_pola, regeneruj_pliki=True):
    """
    Aktualizuje wybrane pola w zgłoszeniu, zapisuje bazę i opcjonalnie regeneruje PDF/JSON.
    Zwraca zaktualizowany rekord lub None.
    """
    szukany = nr_rek.strip().upper().replace("_", "/")
    wszystkie = wczytajDane()
    znaleziono = None

    for r in wszystkie:
        if r.get("nr_rek", "").strip().upper().replace("_", "/") == szukany:
            r.update(zaktualizowane_pola)
            znaleziono = r
            break

    if not znaleziono:
        return None

    zapiszDane(wszystkie)

    if regeneruj_pliki:
        nazwa_folderu = szukany.replace("/", "_")
        folder_docelowy = os.path.join(FOLDER_DANYCH, nazwa_folderu)
        if os.path.exists(folder_docelowy):
            try:
                generujPdf(folder_docelowy, znaleziono, szukany, FOLDER_PROJEKTU)
                generujJSON(folder_docelowy, znaleziono, nazwa_folderu, FOLDER_PROJEKTU)
            except Exception as e:
                print(f"[BŁĄD REGENERACJI PLIKÓW DLA {szukany}]: {e}")

    return znaleziono


def przygotuj_i_kopiuj_zalaczniki(nr_rek, lista_sciezek_zrodlowych, dane_zgloszenia):
    """Tworzy folder zgłoszenia, generuje pliki systemowe (PDF, JSON) i kopiuje załączniki."""
    if not lista_sciezek_zrodlowych:
        lista_sciezek_zrodlowych = []

    nazwa_folderu = nr_rek.replace("/", "_")
    folder_docelowy = os.path.join(FOLDER_DANYCH, nazwa_folderu)
    os.makedirs(folder_docelowy, exist_ok=True)

    zapisane_pliki = []

    # 1. Generowanie PDF
    try:
        sciezka_pdf = generujPdf(
            folder_docelowy, dane_zgloszenia, nr_rek, FOLDER_PROJEKTU
        )
        if sciezka_pdf:
            zapisane_pliki.append(os.path.relpath(sciezka_pdf, FOLDER_PROJEKTU))
    except Exception as e:
        print(f"[BŁĄD GENEROWANIA PDF]: {e}")

    # 2. Generowanie pojedynczego JSON
    try:
        sciezka_json = generujJSON(
            folder_docelowy, dane_zgloszenia, nazwa_folderu, FOLDER_PROJEKTU
        )
        if sciezka_json:
            zapisane_pliki.append(os.path.relpath(sciezka_json, FOLDER_PROJEKTU))
    except Exception as e:
        print(f"[BŁĄD ZAPISU POJEDYNCZEGO JSON]: {e}")

    # 3. Kopiowanie załączników użytkownika
    for sciezka_pliku in lista_sciezek_zrodlowych:
        if os.path.exists(sciezka_pliku):
            nazwa_pliku = os.path.basename(sciezka_pliku)
            sciezka_docelowa = os.path.join(folder_docelowy, nazwa_pliku)

            shutil.copy2(sciezka_pliku, sciezka_docelowa)
            sciezka_wzgledna = os.path.relpath(sciezka_docelowa, FOLDER_PROJEKTU)
            zapisane_pliki.append(sciezka_wzgledna)

    return zapisane_pliki


def dodajReklamacje(nowe_zgloszenie, lista_zalacznikow_sciezki=None):
    """Rejestruje nową reklamację, nadaje numer ID/rok i kopiuje załączniki."""
    if lista_zalacznikow_sciezki is None:
        lista_zalacznikow_sciezki = []

    reklamacje = wczytajDane()

    max_id = max([r.get("id", 0) for r in reklamacje], default=0)
    nowe_id = max_id + 1
    rok = datetime.date.today().year
    nr_rek = f"ZG/{rok}/{nowe_id:03d}"

    nowe_zgloszenie["id"] = nowe_id
    nowe_zgloszenie["nr_rek"] = nr_rek

    sciezki_zalacznikow = przygotuj_i_kopiuj_zalaczniki(
        nr_rek, lista_zalacznikow_sciezki, nowe_zgloszenie
    )
    nowe_zgloszenie["zalaczniki"] = sciezki_zalacznikow

    reklamacje.append(nowe_zgloszenie)
    zapiszDane(reklamacje)

    return nowe_zgloszenie