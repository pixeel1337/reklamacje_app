import datetime
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from baza import dodajReklamacje, wczytajDane
from obsluga_maili import wyslijMaila
from config import DYREKTORZY 


def generuj_nastepny_nr_rek():
    dane = wczytajDane()
    max_id = max([r.get("id", 0) for r in dane], default=0)
    nastepne_id = max_id + 1
    rok = datetime.date.today().year
    return f"ZG/{rok}/{nastepne_id:03d}"


def otworzFormularzDodawania(parent_window, callback_odswiez=None):
    form_window = tk.Toplevel(parent_window)
    form_window.title("Nowe zgłoszenie reklamacyjne")
    form_window.geometry("750x850")
    form_window.configure(bg="#f4f1ea")

    form_window.transient(parent_window)
    form_window.grab_set()

    wybrane_zalaczniki = []
    dzisiaj = datetime.date.today().strftime("%d.%m.%Y")
    nastepny_nr_rek = generuj_nastepny_nr_rek()

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
        text=nastepny_nr_rek,
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

    content_frame = tk.Frame(form_window, bg="#f4f1ea", padx=20)
    content_frame.pack(fill="both", expand=True)

    sec1_card = tk.Frame(content_frame, bg="#f8f6f0", bd=1, relief="solid")
    sec1_card.pack(fill="x", pady=(0, 15))

    card1_body = tk.Frame(sec1_card, bg="#f8f6f0", padx=15, pady=12)
    card1_body.pack(fill="x")
    card1_body.columnconfigure(0, weight=1)
    card1_body.columnconfigure(1, weight=1)

    f_rola = tk.Frame(card1_body, bg="#f8f6f0")
    f_rola.grid(row=0, column=0, sticky="ew", padx=(0, 10))
    tk.Label(
        f_rola,
        text="PRACUJESZ JAKO",
        font=("Segoe UI", 8, "bold"),
        bg="#f8f6f0",
        fg="#64748b",
    ).pack(anchor="w")

    combo_rola = ttk.Combobox(
        f_rola,
        values=["Osoba rejestrująca", "Dyrektor obszaru", "Serwisant"],
        state="readonly",
        font=("Segoe UI", 10),
    )
    combo_rola.set("Osoba rejestrująca")
    combo_rola.pack(fill="x", pady=(4, 0), ipady=3)

    f_osoba = tk.Frame(card1_body, bg="#f8f6f0")
    f_osoba.grid(row=0, column=1, sticky="ew")
    tk.Label(
        f_osoba,
        text="OSOBA REJESTRUJĄCA *",
        font=("Segoe UI", 8, "bold"),
        bg="#f8f6f0",
        fg="#64748b",
    ).pack(anchor="w")
    e_osoba = tk.Entry(f_osoba, font=("Segoe UI", 10), bd=1, relief="solid")
    e_osoba.insert(0, "Jan Kowalski")
    e_osoba.pack(fill="x", ipady=4, pady=(4, 0))

    sec2_card = tk.Frame(content_frame, bg="#ffffff", bd=1, relief="solid")
    sec2_card.pack(fill="both", expand=True, pady=(0, 20))

    card2_body = tk.Frame(sec2_card, bg="#ffffff", padx=20, pady=15)
    card2_body.pack(fill="both", expand=True)

    tk.Label(
        card2_body,
        text="❶  1 · REJESTRACJA ZGŁOSZENIA",
        font=("Segoe UI", 11, "bold"),
        bg="#ffffff",
        fg="#0f172a",
    ).pack(anchor="w", pady=(0, 12))

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

    f_klient = tk.Frame(row1, bg="#ffffff")
    f_klient.grid(row=0, column=1, sticky="ew")
    tk.Label(
        f_klient,
        text="KLIENT *",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#b91c1c",
    ).pack(anchor="w")
    e_klient = tk.Entry(f_klient, font=("Segoe UI", 10), bd=1, relief="solid")
    e_klient.pack(fill="x", ipady=4, pady=(3, 0))

    row2 = tk.Frame(card2_body, bg="#ffffff")
    row2.pack(fill="x", pady=(0, 10))
    row2.columnconfigure(0, weight=1)
    row2.columnconfigure(1, weight=1)

    f_projekt = tk.Frame(row2, bg="#ffffff")
    f_projekt.grid(row=0, column=0, sticky="ew", padx=(0, 10))
    tk.Label(
        f_projekt,
        text="NR PROJEKTU / ZADANIA *",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#b91c1c",
    ).pack(anchor="w")
    e_projekt = tk.Entry(f_projekt, font=("Segoe UI", 10), bd=1, relief="solid")
    e_projekt.pack(fill="x", ipady=4, pady=(3, 0))

    f_dyrektor = tk.Frame(row2, bg="#ffffff")
    f_dyrektor.grid(row=0, column=1, sticky="ew")
    tk.Label(
        f_dyrektor,
        text="DYREKTOR OBSZARU *",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#b91c1c",
    ).pack(anchor="w")

    
    combo_dyrektor = ttk.Combobox(
        f_dyrektor, values=DYREKTORZY, font=("Segoe UI", 10), state="readonly"
    )
    combo_dyrektor.set(DYREKTORZY[0])
    combo_dyrektor.pack(fill="x", ipady=3, pady=(3, 0))

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

    row4 = tk.Frame(card2_body, bg="#ffffff")
    row4.pack(fill="x", pady=(0, 15))
    tk.Label(
        row4,
        text="ZAŁĄCZNIKI (PLIKI / ZDJĘCIA)",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#64748b",
    ).pack(anchor="w")

    zalaczniki_frame = tk.Frame(row4, bg="#ffffff")
    zalaczniki_frame.pack(fill="x", pady=(3, 5))

    def usunZalacznik(sciezka):
        if sciezka in wybrane_zalaczniki:
            wybrane_zalaczniki.remove(sciezka)
            odswiezWidokZalacznikow()

    def odswiezWidokZalacznikow():
        for w in zalaczniki_frame.winfo_children():
            w.destroy()

        for f in wybrane_zalaczniki:
            nazwa_pliku = os.path.basename(f)
            item_row = tk.Frame(zalaczniki_frame, bg="#f1f5f9", pady=2, padx=5)
            item_row.pack(fill="x", pady=2)

            tk.Label(
                item_row,
                text=f"📎 {nazwa_pliku}",
                font=("Segoe UI", 9),
                bg="#f1f5f9",
                fg="#334155",
                anchor="w",
            ).pack(side="left", fill="x", expand=True)

            btn_del = tk.Button(
                item_row,
                text="✕",
                font=("Segoe UI", 8, "bold"),
                bg="#f1f5f9",
                fg="#b91c1c",
                bd=0,
                cursor="hand2",
                command=lambda p=f: usunZalacznik(p),
            )
            btn_del.pack(side="right", padx=5)

    def dodajPliki():
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
            odswiezWidokZalacznikow()

    btn_dodaj_plik = tk.Button(
        row4,
        text="+ Dodaj plik",
        font=("Segoe UI", 8, "bold"),
        bg="#e2e8f0",
        fg="#334155",
        bd=0,
        padx=10,
        pady=4,
        cursor="hand2",
        command=dodajPliki,
    )
    btn_dodaj_plik.pack(anchor="w", pady=(2, 0))

    def obsluzZapis():
        klient = e_klient.get().strip()
        nr_projektu = e_projekt.get().strip()
        opis = txt_opis.get("1.0", tk.END).strip()
        dyrektor = combo_dyrektor.get()
        osoba_rejestrujaca = e_osoba.get().strip()

        if not klient or not nr_projektu or not opis or not osoba_rejestrujaca:
            messagebox.showwarning(
                "Brakujące dane!",
                "Wypełnij wszystkie pola oznaczone gwiazdką (*)! ",
                parent=form_window,
            )
            return

        nowe = {
            "nr_rek": nastepny_nr_rek,
            "data_zgl": e_data.get().strip(),
            "klient": klient,
            "nr_projektu": nr_projektu,
            "nr_zadania": nr_projektu,
            "opis": opis,
            "pracujesz_jako": combo_rola.get(),
            "osoba_rejestrujaca": osoba_rejestrujaca,
            "dyrektor": dyrektor,
            "odpowiedzialny": "—",
            "status": "NOWE",
        }

        dodajReklamacje(nowe, wybrane_zalaczniki)

        threading.Thread(
            target=wyslijMaila,
            kwargs={
                "odbiorca": dyrektor,
                "nr_rek": nastepny_nr_rek,
                "klient": klient,
                "nr_projektu": nr_projektu,
                "opis": opis,
                "typ": "dyrektor",
            },
            daemon=True,
        ).start()

        messagebox.showinfo(
            "Sukces",
            f"Pomyślnie dodano zgłoszenie {nastepny_nr_rek} oraz wysłano powiadomienie e-mail do: {dyrektor}!",
            parent=form_window,
        )

        if callable(callback_odswiez):
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

    return form_window


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    panel = otworzFormularzDodawania(root)
    panel.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()