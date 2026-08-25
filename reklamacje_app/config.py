import os
from obsluga_maili import MAPA_EMAILI

# --- ŚCIEŻKI SYSTEMOWE ---
FOLDER_PROJEKTU = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(FOLDER_PROJEKTU, "reklamacje.json")
FOLDER_DANYCH = os.path.join(FOLDER_PROJEKTU, "Reklamacje_Dane")

# --- PERSONEL I ROLE ---
PRACOWNICY = (
    list(MAPA_EMAILI.keys())
    if MAPA_EMAILI
    else [
        "Marek Zieliński",
        "Piotr Kowalski",
        "Marta Wiśniewska",
        "Jan Kowalski",
        "Anna Nowak",
    ]
)

DYREKTORZY = [
    "Anna Kowalska",
    "Marek Nowak",
    "Piotr Wiśniewski",
]

# --- PALETA KOLORÓW I MOTYW UI ---
KOLORY = {
    "tlo_glowne": "#eef2f5",
    "tlo_panele": "#f4f1ea",
    "tlo_karty": "#ffffff",
    "tlo_sekcji": "#f8f6f0",
    "glowny_akcent": "#1f4e5b",
    "akcent_hover": "#2d6a78",
    "tekst_ciemny": "#0f172a",
    "tekst_szary": "#64748b",
    "sukces": "#16a34a",
    "blad": "#dc2626",
    "ostrzezenie": "#d97706",
}

# --- STATUSY ---
STATUSY_OTWARTE = [
    "NOWE",
    "W TRAKCIE",
    "CZEKA NA ZAMKNIĘCIE",
    "PRZEKAZANE DO REALIZACJI",
]