import datetime
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from baza import dodajReklamacje


def otworzFormularzDodawania(parent_window, callback_odswiez=None):
    form_window = tk.Toplevel(parent_window)
    form_window.title("Nowe zgłoszenie")
    form_window.geometry("750x850")
    form_window.configure(bg="#f4f1ea")

    form_window.transient(parent_window)
    form_window.grab_set()

    dzisiaj = datetime.date.today().strftime("%d.%m.%Y")

    # Lista na przechowywanie ścieżek do wybranych załączników
    wybrane_zalaczniki = []

    # --- PASEK GÓRNY ---
    top_bar = tk.Frame(form_window, bg="#f4f1ea", padx=20, pady=15)
    top_bar.pack(fill="x")

    btn_back = tk.Button(
        top_bar,
        text="← Wróć do rejestru",
        font=("Segoe UI", 10, "bold"),
        bg="#f4f1ea",
        fg="#1f4e5b",
        bd=0,
        cursor="hand2",
        command=form_window.destroy,
    )
    btn_back.pack(side="left")

    nr_badge_frame = tk.Frame(top_bar, bg="#f4f1ea")
    nr_badge_frame.pack(side="right")

    lbl_nr = tk.Label(
        nr_badge_frame,
        text="ZG/NOWE",
        font=("Segoe UI", 10, "bold"),
        bg="#f4f1ea",
        fg="#334155",
    )
    lbl_nr.pack(side="left", padx=(0, 5))

    lbl_status = tk.Label(
        nr_badge_frame,
        text=" NOWE ",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#1f4e5b",
        relief="solid",
        bd=1,
    )
    lbl_status.pack(side="left")

    content_frame = tk.Frame(form_window, bg="#f8f6f0", padx=20)
    content_frame.pack(fill="both", expand=True)

    # --- KAFELEK PRACOWNIKA ---
    sec1_card = tk.Frame(content_frame, bg="#f8f6f0", bd=1, relief="solid")
    sec1_card.pack(fill="x", pady=(0, 15), ipady=5)

    card1_body = tk.Frame(content_frame, bg="#f8f6f0", padx=15, pady=10)
    card1_body.pack(fill="x")

    tk.Label(
        card1_body,
        text="Osoba rejestrująca",
        font=("Segoe UI", 8, "bold"),
        bg="#f8f6f0",
        fg="#64748b",
    ).pack(anchor="w")

    combo_rola = ttk.Combobox(
        card1_body,
        values=["Osoba rejestrująca", "Dyrektor obszaru", "Serwisant"],
        state="readonly",
        font=("Segoe UI", 10),
    )
    combo_rola.set("Osoba rejestrująca")
    combo_rola.pack(fill="x", pady=(5, 0), ipady=3)

    # --- REJESTRACJA ZGŁOSZENIA ---
    sec2_card = tk.Frame(content_frame, bg="#ffffff", bd=1, relief="solid")
    sec2_card.pack(fill="both", expand=True, pady=(0, 20))

    card2_body = tk.Frame(sec2_card, bg="#ffffff", padx=20, pady=15)
    card2_body.pack(fill="both", expand=True)

    sec2_title = tk.Label(
        card2_body,
        text="❶  1 · REJESTRACJA ZGŁOSZENIA",
        font=("Segoe UI", 11, "bold"),
        bg="#ffffff",
        fg="#0f172a",
    )
    sec2_title.pack(anchor="w", pady=(0, 15))

    # Wiersz 1: Data + Osoba
    row1 = tk.Frame(card2_body, bg="#ffffff")
    row1.pack(fill="x", pady=(0, 10))
    row1.columnconfigure(0, weight=1)
    row1.columnconfigure(1, weight=1)

    f_data = tk.Frame(row1, bg="#ffffff")
    f_data.grid(row=0, column=0, sticky="ew", padx=(0, 10))
    tk.Label(
        f_data,
        text="DATA WPŁYNIĘCIA",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#64748b",
    ).pack(anchor="w")
    e_data = tk.Entry(f_data, font=("Segoe UI", 10), bd=1, relief="solid")
    e_data.insert(0, dzisiaj)
    e_data.pack(fill="x", ipady=4, pady=(3, 0))

    f_osoba = tk.Frame(row1, bg="#ffffff")
    f_osoba.grid(row=0, column=1, sticky="ew")
    tk.Label(
        f_osoba,
        text="OSOBA REJESTRUJĄCA",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#64748b",
    ).pack(anchor="w")
    e_osoba = tk.Entry(f_osoba, font=("Segoe UI", 10), bd=1, relief="solid")
    e_osoba.insert(0, "Franciszek Wrona")
    e_osoba.pack(fill="x", ipady=4, pady=(3, 0))

    # Wiersz 2: Klient + Nr Projektu
    row2 = tk.Frame(card2_body, bg="#ffffff")
    row2.pack(fill="x", pady=(0, 10))
    row2.columnconfigure(0, weight=1)
    row2.columnconfigure(1, weight=1)

    f_klient = tk.Frame(row2, bg="#ffffff")
    f_klient.grid(row=0, column=0, sticky="ew", padx=(0, 10))
    tk.Label(
        f_klient,
        text="KLIENT * ",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#b91c1c",
    ).pack(anchor="w")
    e_klient = tk.Entry(f_klient, font=("Segoe UI", 10), bd=1, relief="solid")
    e_klient.pack(fill="x", ipady=4, pady=(3, 0))

    f_projekt = tk.Frame(row2, bg="#ffffff")
    f_projekt.grid(row=0, column=1, sticky="ew")
    tk.Label(
        f_projekt,
        text="NR PROJEKTU *",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#b91c1c",
    ).pack(anchor="w")
    e_projekt = tk.Entry(f_projekt, font=("Segoe UI", 10), bd=1, relief="solid")
    e_projekt.pack(fill="x", ipady=4, pady=(3, 0))

    # Wiersz 3: Opis Zgłoszenia
    row3 = tk.Frame(card2_body, bg="#ffffff")
    row3.pack(fill="x", pady=(0, 10))
    tk.Label(
        row3,
        text="OPIS ZGŁOSZENIA *",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#b91c1c",
    ).pack(anchor="w")
    txt_opis = tk.Text(row3, font=("Segoe UI", 10), height=3, bd=1, relief="solid")
    txt_opis.pack(fill="x", pady=(3, 0))

    # Wiersz 4: Dyrektor Obszaru
    row4 = tk.Frame(card2_body, bg="#ffffff")
    row4.pack(fill="x", pady=(0, 15))
    tk.Label(
        row4,
        text="DYREKTOR OBSZARU *",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#b91c1c",
    ).pack(anchor="w")
    combo_dyrektor = ttk.Combobox(
        row4,
        values=["Anna Kowalska", "Marek Nowak", "Piotr Wiśniewski"],
        font=("Segoe UI", 10),
    )
    combo_dyrektor.set("Anna Kowalska")
    combo_dyrektor.pack(fill="x", ipady=3, pady=(3, 0))

    # Wiersz 5: OBSŁUGA ZAŁĄCZNIKÓW
    row5 = tk.Frame(card2_body, bg="#ffffff")
    row5.pack(fill="x", pady=(0, 15))

    tk.Label(
        row5,
        text="ZAŁĄCZNIKI",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#64748b",
    ).pack(anchor="w")

    # Kontener na dynamiczną listę wybranych plików
    frame_lista_plikow = tk.Frame(row5, bg="#ffffff")
    frame_lista_plikow.pack(fill="x", pady=(3, 5))

    def odswiez_widok_zalacznikow():
        """Czyści i na nowo rysuje etykiety dodanych plików."""
        for widget in frame_lista_plikow.winfo_children():
            widget.destroy()

        for idx, plik in enumerate(wybrane_zalaczniki):
            nazwa_pliku = os.path.basename(plik)
            lbl = tk.Label(
                frame_lista_plikow,
                text=f" 📎 {nazwa_pliku}",
                font=("Segoe UI", 9),
                bg="#f1f5f9",
                fg="#334155",
                anchor="w",
                pady=4,
            )
            lbl.pack(fill="x", pady=2)

    def dodaj_pliki():
        """Otwiera okno dialogowe systemu do wyboru plików."""
        sciezki = filedialog.askopenfilenames(
            title="Wybierz załączniki",
            filetypes=[
                ("Wszystkie pliki", "*.*"),
                ("Dokumenty PDF", "*.pdf"),
                ("Zdjęcia", "*.png;*.jpg;*.jpeg"),
            ],
        )
        if sciezki:
            for sciezka in sciezki:
                if sciezka not in wybrane_zalaczniki:
                    wybrane_zalaczniki.append(sciezka)
            odswiez_widok_zalacznikow()

    btn_dodaj_plik = tk.Button(
        row5,
        text="+ Dodaj plik",
        font=("Segoe UI", 8, "bold"),
        bg="#e2e8f0",
        fg="#334155",
        bd=0,
        padx=10,
        pady=4,
        cursor="hand2",
        command=dodaj_pliki,
    )
    btn_dodaj_plik.pack(anchor="w", pady=(2, 0))

    # --- LOGIKA ZAPISU ---
    def obsluzZapis():
        klient = e_klient.get().strip()
        nr_projektu = e_projekt.get().strip()
        opis = txt_opis.get("1.0", tk.END).strip()

        if not klient or not nr_projektu or not opis:
            messagebox.showwarning(
                "Puste pola",
                "Wypełnij wszystkie pola z czerwoną gwiazdką (*)! ",
                parent=form_window,
            )
            return

        # Zapisujemy same nazwy plików (lub pełne ścieżki)
        nazwy_zalacznikow = [os.path.basename(p) for p in wybrane_zalaczniki]

        nowe = {
            "data_zgl": e_data.get().strip(),
            "klient": klient,
            "nr_projektu": nr_projektu,
            "opis": opis,
            "pracujesz_jako": combo_rola.get(),
            "osoba_rejestrujaca": e_osoba.get().strip(),
            "dyrektor": combo_dyrektor.get(),
            "odpowiedzialny": "—",
            "status": "NOWE",
            "zalaczniki": nazwy_zalacznikow,
        }

        dodajReklamacje(nowe)

        messagebox.showinfo(
            "Sukces", "Zgłoszenie zostało dodane!", parent=form_window
        )

        if callback_odswiez:
            callback_odswiez()

        form_window.destroy()

    btn_send = tk.Button(
        card2_body,
        text="✉ Wyślij do dyrektora",
        font=("Segoe UI", 10, "bold"),
        bg="#1f4e5b",
        fg="white",
        activebackground="#2d6a78",
        activeforeground="white",
        bd=0,
        padx=15,
        pady=8,
        cursor="hand2",
        command=obsluzZapis,
    )
    btn_send.pack(anchor="w", pady=(10, 0))