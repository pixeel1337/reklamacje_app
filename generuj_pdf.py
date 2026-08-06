import os
from fpdf import FPDF

def generujPdf(folder_docelowy, dane, nr_rek, folder_projektu):
    pdf = FPDF()
    pdf.add_page()

    sciezka_czcionki = r"C:\Windows\Fonts\arial.ttf"
    if os.path.exists(sciezka_czcionki):
        pdf.add_font("ArialPL", "", sciezka_czcionki)
        pdf.set_font("ArialPL", size=12)
    else:
        pdf.set_font("Helvetica", size=12)


    # Baner ORLEN PROJEKT
    pdf.set_text_color(220, 38, 38)  
    pdf.set_font_size(22)
    pdf.cell(
        0, 12, text="ORLEN PROJEKT", new_x="LMARGIN", new_y="NEXT", align="C"
    )

    pdf.set_draw_color(220, 38, 38)
    pdf.set_line_width(1)
    pdf.line(10, pdf.get_y() + 2, 200, pdf.get_y() + 2)
    pdf.ln(10)

    # Tytuł zgłoszenia
    pdf.set_text_color(15, 23, 42)
    pdf.set_font_size(14)
    pdf.cell(
        0,
        10,
        text=f"KARTA ZGŁOSZENIA REKLAMACYJNEGO: {nr_rek}",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(4)

    # Dane zgłoszenia
    pdf.set_font_size(10)
    pola = [
        ("Data zgłoszenia:", dane.get("data_zgl", "—")),
        ("Klient / Firma:", dane.get("klient", "—")),
        ("Numer projektu:", dane.get("nr_projektu", "—")),
        ("Rola zgłaszającego:", dane.get("pracujesz_jako", "—")),
        ("Osoba rejestrująca:", dane.get("osoba_rejestrujaca", "—")),
        ("Dyrektor odpowiedzialny:", dane.get("dyrektor", "—")),
        ("Status zgłoszenia:", dane.get("status", "NOWE")),
    ]

    for label, val in pola:
        pdf.set_text_color(100, 116, 139)  
        pdf.cell(50, 7, text=label, new_x="RIGHT", new_y="TOP")
        pdf.set_text_color(15, 23, 42)  
        pdf.multi_cell(0, 7, text=str(val), new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)

    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 7, text="Opis zgłoszenia / problemu:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(15, 23, 42)
    pdf.multi_cell(0, 6, text=dane.get("opis", "—"))

    nazwa_pdf = f"{nr_rek.replace('/', '_')}_KARTA.pdf"
    sciezka_pdf = os.path.join(folder_docelowy, nazwa_pdf)
    pdf.output(sciezka_pdf)

    return os.path.relpath(sciezka_pdf, folder_projektu)