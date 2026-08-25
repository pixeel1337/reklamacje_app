import os
from fpdf import FPDF


def generujPdf(folder_docelowy, dane, nr_rek, folder_projektu):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Bezpieczne ładowanie czcionki z polskimi znakami
    sciezka_czcionki = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "arial.ttf")
    if os.path.exists(sciezka_czcionki):
        pdf.add_font("ArialPL", "", sciezka_czcionki)
        pdf.add_font("ArialPL", "B", os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "arialbd.ttf") if os.path.exists(os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "arialbd.ttf")) else sciezka_czcionki)
        font_family = "ArialPL"
    else:
        font_family = "Helvetica"

    pdf.set_font(font_family, size=12)

    # Baner firmowy
    pdf.set_text_color(220, 38, 38)
    pdf.set_font(font_family, style="B" if font_family == "ArialPL" else "", size=20)
    pdf.cell(0, 10, text="ORLEN PROJEKT", new_x="LMARGIN", new_y="NEXT", align="C")

    # Czerwona linia dekoracyjna pod banerem
    pdf.set_draw_color(220, 38, 38)
    pdf.set_line_width(0.8)
    pdf.line(pdf.l_margin, pdf.get_y() + 2, pdf.w - pdf.r_margin, pdf.get_y() + 2)
    pdf.ln(8)

    # Tytuł zgłoszenia ze statusem
    status = dane.get("status", "NOWE")
    pdf.set_text_color(15, 23, 42)
    pdf.set_font(font_family, style="B" if font_family == "ArialPL" else "", size=13)
    pdf.cell(0, 8, text=f"KARTA ZGŁOSZENIA REKLAMACYJNEGO: {nr_rek}", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font(font_family, size=9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, text=f"STATUS: {status.upper()}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # --- SEKCJA 1: PODSTAWOWE DANE ---
    nr_proj = dane.get("nr_projektu") or dane.get("nr_zadania") or "—"
    pola_podstawowe = [
        ("Data zgłoszenia:", dane.get("data_zgl", "—")),
        ("Klient / Firma:", dane.get("klient", "—")),
        ("Numer projektu/zadania:", nr_proj),
        ("Rola zgłaszającego:", dane.get("pracujesz_jako", "—")),
        ("Osoba rejestrująca:", dane.get("osoba_rejestrujaca", "—")),
        ("Dyrektor obszaru:", dane.get("dyrektor", "—")),
        ("Osoba odpowiedzialna:", dane.get("odpowiedzialny", "—")),
    ]

    for label, val in pola_podstawowe:
        pdf.set_text_color(100, 116, 139)
        pdf.set_font(font_family, size=9)
        pdf.cell(50, 6, text=label, new_x="RIGHT", new_y="TOP")
        pdf.set_text_color(15, 23, 42)
        pdf.multi_cell(0, 6, text=str(val), new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)

    # --- SEKCJA 2: OPIS ZGŁOSZENIA ---
    pdf.set_text_color(100, 116, 139)
    pdf.set_font(font_family, style="B" if font_family == "ArialPL" else "", size=9)
    pdf.cell(0, 6, text="OPIS PROBLEMU / ZGŁOSZENIA:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(font_family, size=9)
    pdf.set_text_color(15, 23, 42)
    pdf.multi_cell(0, 5, text=dane.get("opis", "—"))
    pdf.ln(4)

    # --- SEKCJA 3: DECYZJA DYREKTORA (JEŚLI ODRZUCONO) ---
    if status == "ODRZUCONE" or dane.get("powod_odrzucenia"):
        pdf.set_draw_color(239, 68, 68)
        pdf.set_fill_color(254, 242, 242)
        pdf.set_text_color(185, 28, 28)
        pdf.set_font(font_family, style="B" if font_family == "ArialPL" else "", size=9)
        pdf.cell(0, 6, text="DECYZJA DYREKTORA - ODRZUCENIE ZGŁOSZENIA:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(font_family, size=9)
        pdf.set_text_color(15, 23, 42)
        pdf.multi_cell(0, 5, text=f"Powód: {dane.get('powod_odrzucenia', '—')}")
        pdf.ln(4)

    # --- SEKCJA 4: REALIZACJA (JEŚLI UZUPEŁNIONA) ---
    if dane.get("opis_dzialan") or dane.get("status_realizacji"):
        pdf.set_text_color(31, 78, 91)
        pdf.set_font(font_family, style="B" if font_family == "ArialPL" else "", size=9)
        pdf.cell(0, 6, text="REALIZACJA I ROZPATRZENIE REKLAMACJI:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(font_family, size=9)
        pdf.set_text_color(15, 23, 42)
        if dane.get("status_realizacji"):
            pdf.cell(50, 5, text="Status realizacji:", new_x="RIGHT", new_y="TOP")
            pdf.multi_cell(0, 5, text=str(dane.get("status_realizacji")), new_x="LMARGIN", new_y="NEXT")
        if dane.get("opis_dzialan"):
            pdf.cell(50, 5, text="Podjęte działania:", new_x="RIGHT", new_y="TOP")
            pdf.multi_cell(0, 5, text=str(dane.get("opis_dzialan")), new_x="LMARGIN", new_y="NEXT")

    # Zapis pliku
    nazwa_pdf = f"{nr_rek.replace('/', '_')}_KARTA.pdf"
    sciezka_pdf = os.path.join(folder_docelowy, nazwa_pdf)
    pdf.output(sciezka_pdf)

    return os.path.relpath(sciezka_pdf, folder_projektu)