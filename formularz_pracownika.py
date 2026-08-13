import os
import tkinter as tk
from tkinter import messagebox, ttk

from baza import wczytajDane, zapiszDane
from generuj_json import generujJSON
from generuj_pdf import generujPdf


def otworzPanelRealizacji(parent_window, nr_rek_start="ZG/2026/001", odswiez_callback=None):
    win = tk.Toplevel(parent_window)
    win.title("Realizacja zgłoszenia - Panel Pracownika")
    win.geometry("780x920")
    win.configure(bg="#f4f1ea")

    win.transient(parent_window)
    win.grab_set()

    aktualna_reklamacja = {}

    # TOP BAR z polem wyszukiwania numeru
    top_bar = tk.Frame(win, bg="#f4f1ea", padx=20, pady=15)
    top_bar.pack(fill="x")

    btn_back = tk.Button(
        top_bar,
        text="← Wróć do rejestru",
        font=("Segoe UI", 10, "bold"),
        bg="#f4f1ea",
        fg="#1f4e5b",
        bd=0,
        cursor="hand2",
        command=win.destroy,
    )
    btn_back.pack(side="left")

    search_box = tk.Frame(top_bar, bg="#f4f1ea")
    search_box.pack(side="right")

    tk.Label(
        search_box,
        text="NR REKLAMACJI:",
        font=("Segoe UI", 8, "bold"),
        bg="#f4f1ea",
        fg="#64748b",
    ).pack(side="left", padx=(0, 5))

    e_szukaj_nr = tk.Entry(
        search_box, font=("Segoe UI", 9, "bold"), width=14, bd=1, relief="solid"
    )
    e_szukaj_nr.insert(0, nr_rek_start)
    e_szukaj_nr.pack(side="left", ipady=2, padx=(0, 5))

    lbl_status_badge = tk.Label(
        search_box,
        text=" NOWE ",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#d97706",
        relief="solid",
        bd=1,
    )

    btn_laduj = tk.Button(
        search_box,
        text="🔍 Wczytaj",
        font=("Segoe UI", 8, "bold"),
        bg="#1f4e5b",
        fg="white",
        bd=0,
        padx=8,
        pady=3,
        cursor="hand2",
    )

    lbl_status_badge.pack(side="right", padx=(5, 0))
    btn_laduj.pack(side="right")

    # Canvas ze scrollem
    canvas = tk.Canvas(win, bg="#f4f1ea", highlightthickness=0)
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f4f1ea", padx=20)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=720)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # KAFELEK 1: Rola i użytkownik
    sec1_card = tk.Frame(scroll_frame, bg="#f8f6f0", padx=15, pady=12)
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

    combo_pracujesz = ttk.Combobox(
        f_rola,
        values=["Osoba odpowiedzialna"],
        state="readonly",
        font=("Segoe UI", 10),
    )
    combo_pracujesz.set("Osoba odpowiedzialna")
    combo_pracujesz.pack(fill="x", pady=(3, 0), ipady=2)

    f_zalogowany = tk.Frame(card1_body, bg="#f8f6f0")
    f_zalogowany.grid(row=0, column=1, sticky="ew")
    tk.Label(
        f_zalogowany,
        text="ZALOGOWANY JAKO (OSOBA ODPOWIEDZIALNA)",
        font=("Segoe UI", 8, "bold"),
        bg="#f8f6f0",
        fg="#64748b",
    ).pack(anchor="w")

    combo_zalogowany = ttk.Combobox(
        f_zalogowany,
        values=["Marek Zieliński"],
        state="readonly",
        font=("Segoe UI", 10),
    )
    combo_zalogowany.set("Marek Zieliński")
    combo_zalogowany.pack(fill="x", pady=(3, 0), ipady=2)

    # KAFELEK 2: REALIZACJA I ZAMKNIĘCIE
    sec2_card = tk.Frame(scroll_frame, bg="#ffffff", bd=1, relief="solid")
    sec2_card.pack(fill="x", pady=(0, 20))

    card2_body = tk.Frame(sec2_card, bg="#ffffff", padx=20, pady=15)
    card2_body.pack(fill="x")

    sec2_title = tk.Label(
        card2_body,
        text="⚙ 3 · REALIZACJA I ZAMKNIĘCIE",
        font=("Segoe UI", 11, "bold"),
        bg="#ffffff",
        fg="#0f172a",
    )
    sec2_title.pack(anchor="w", pady=(0, 10))

    lbl_osoba_odp = tk.Label(
        card2_body,
        text="Osoba odpowiedzialna: Marek Zieliński",
        font=("Segoe UI", 9, "bold"),
        bg="#ffffff",
        fg="#0f172a",
    )
    lbl_osoba_odp.pack(anchor="w", pady=(0, 10))

    # SPOSÓB ZAŁATWIENIA SPRAWY (Przyciskowy wybór)
    tk.Label(
        card2_body,
        text="SPOSÓB ZAŁATWIENIA SPRAWY *",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#b91c1c",
    ).pack(anchor="w")

    sposob_var = tk.StringVar(value="UZNANO CZĘŚCIOWO")
    f_sposob_btn = tk.Frame(card2_body, bg="#ffffff")
    f_sposob_btn.pack(anchor="w", pady=(5, 15))

    btn_uznano = tk.Button(
        f_sposob_btn,
        text="UZNANO",
        font=("Segoe UI", 8, "bold"),
        bd=1,
        relief="solid",
        padx=12,
        pady=4,
    )
    btn_czesciowo = tk.Button(
        f_sposob_btn,
        text="UZNANO CZĘŚCIOWO",
        font=("Segoe UI", 8, "bold"),
        bd=1,
        relief="solid",
        padx=12,
        pady=4,
    )
    btn_nieuznano = tk.Button(
        f_sposob_btn,
        text="NIE UZNANO",
        font=("Segoe UI", 8, "bold"),
        bd=1,
        relief="solid",
        padx=12,
        pady=4,
    )

    def ustaw_sposob(val):
        sposob_var.set(val)
        btn_uznano.config(
            bg="#b45309" if val == "UZNANO" else "#ffffff",
            fg="white" if val == "UZNANO" else "#475569",
        )
        btn_czesciowo.config(
            bg="#b45309" if val in ["UZNANO CZĘŚCIOWO", "UZNANO CZEŚCIOWO"] else "#ffffff",
            fg="white" if val in ["UZNANO CZĘŚCIOWO", "UZNANO CZEŚCIOWO"] else "#475569",
        )
        btn_nieuznano.config(
            bg="#b45309" if val == "NIE UZNANO" else "#ffffff",
            fg="white" if val == "NIE UZNANO" else "#475569",
        )

    btn_uznano.config(command=lambda: ustaw_sposob("UZNANO"))
    btn_czesciowo.config(command=lambda: ustaw_sposob("UZNANO CZĘŚCIOWO"))
    btn_nieuznano.config(command=lambda: ustaw_sposob("NIE UZNANO"))

    btn_uznano.pack(side="left", padx=(0, 10))
    btn_czesciowo.pack(side="left", padx=(0, 10))
    btn_nieuznano.pack(side="left")

    # SEKCJA TERMINÓW (OPCJONALNA Z CHECKBOXEM)
    f_term_container = tk.Frame(card2_body, bg="#ffffff")
    f_term_container.pack(fill="x", pady=(0, 15))

    wydluzenie_var = tk.BooleanVar(value=False)

    chk_wydluzenie = tk.Checkbutton(
        f_term_container,
        text="Czy termin uległ wydłużeniu?",
        variable=wydluzenie_var,
        font=("Segoe UI", 9, "bold"),
        bg="#ffffff",
        fg="#1f4e5b",
        activebackground="#ffffff",
        selectcolor="#ffffff",
        cursor="hand2",
    )
    chk_wydluzenie.pack(anchor="w", pady=(0, 5))

    f_termDateTime = tk.Frame(
        f_term_container, bg="#f8fafc", bd=1, relief="solid", padx=12, pady=12
    )

    row_term = tk.Frame(f_termDateTime, bg="#f8fafc")
    row_term.pack(fill="x", pady=(0, 8))
    row_term.columnconfigure(0, weight=1)
    row_term.columnconfigure(1, weight=1)

    f_t_std = tk.Frame(row_term, bg="#f8fafc")
    f_t_std.grid(row=0, column=0, sticky="ew", padx=(0, 10))
    tk.Label(
        f_t_std,
        text="TERMIN STANDARDOWY",
        font=("Segoe UI", 8, "bold"),
        bg="#f8fafc",
        fg="#64748b",
    ).pack(anchor="w")
    e_term_std = tk.Entry(f_t_std, font=("Segoe UI", 10), bd=1, relief="solid")
    e_term_std.pack(fill="x", ipady=3, pady=(2, 0))

    f_t_akt = tk.Frame(row_term, bg="#f8fafc")
    f_t_akt.grid(row=0, column=1, sticky="ew")
    tk.Label(
        f_t_akt,
        text="AKTUALNY TERMIN",
        font=("Segoe UI", 8, "bold"),
        bg="#f8fafc",
        fg="#64748b",
    ).pack(anchor="w")
    e_term_akt = tk.Entry(f_t_akt, font=("Segoe UI", 10), bd=1, relief="solid")
    e_term_akt.pack(fill="x", ipady=3, pady=(2, 0))

    tk.Label(
        f_termDateTime,
        text="UZASADNIENIE WYDŁUŻENIA TERMINU *",
        font=("Segoe UI", 8, "bold"),
        bg="#f8fafc",
        fg="#b91c1c",
    ).pack(anchor="w", pady=(5, 0))
    txt_uzasadnienie = tk.Text(
        f_termDateTime, font=("Segoe UI", 9), height=2, bd=1, relief="solid"
    )
    txt_uzasadnienie.pack(fill="x", pady=(2, 0))

    def przełącz_widok_terminu():
        if wydluzenie_var.get():
            f_termDateTime.pack(fill="x", pady=(5, 0))
        else:
            f_termDateTime.pack_forget()

    chk_wydluzenie.config(command=przełącz_widok_terminu)

    # PODWYKONAWCA
    tk.Label(
        card2_body,
        text="CZY DOTYCZY PODWYKONAWCY?",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#64748b",
    ).pack(anchor="w")
    podwykonawca_var = tk.StringVar(value="TAK")

    f_podw_btn = tk.Frame(card2_body, bg="#ffffff")
    f_podw_btn.pack(anchor="w", pady=(3, 10))

    btn_podw_tak = tk.Button(
        f_podw_btn, text="TAK", font=("Segoe UI", 8, "bold"), bd=1, relief="solid", padx=14, pady=2
    )
    btn_podw_nie = tk.Button(
        f_podw_btn, text="NIE", font=("Segoe UI", 8, "bold"), bd=1, relief="solid", padx=14, pady=2
    )

    def ustaw_podw(val):
        podwykonawca_var.set(val)
        btn_podw_tak.config(
            bg="#1f4e5b" if val == "TAK" else "#ffffff",
            fg="white" if val == "TAK" else "#475569",
        )
        btn_podw_nie.config(
            bg="#1f4e5b" if val == "NIE" else "#ffffff",
            fg="white" if val == "NIE" else "#475569",
        )

    btn_podw_tak.config(command=lambda: ustaw_podw("TAK"))
    btn_podw_nie.config(command=lambda: ustaw_podw("NIE"))
    btn_podw_tak.pack(side="left", padx=(0, 5))
    btn_podw_nie.pack(side="left")

    tk.Label(
        card2_body, text="NAZWA PODWYKONAWCY", font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#64748b"
    ).pack(anchor="w")
    e_podwykonawca = tk.Entry(card2_body, font=("Segoe UI", 10), bd=1, relief="solid")
    e_podwykonawca.pack(fill="x", ipady=3, pady=(2, 10))

    # KOSZTY + DATA ZAŁATWIENIA
    row_koszt = tk.Frame(card2_body, bg="#ffffff")
    row_koszt.pack(fill="x", pady=(0, 10))
    row_koszt.columnconfigure(0, weight=1)
    row_koszt.columnconfigure(1, weight=1)

    f_k = tk.Frame(row_koszt, bg="#ffffff")
    f_k.grid(row=0, column=0, sticky="ew", padx=(0, 10))
    tk.Label(
        f_k, text="KOSZTY NAPRAWY (ZŁ)", font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#64748b"
    ).pack(anchor="w")
    e_koszt = tk.Entry(f_k, font=("Segoe UI", 10), bd=1, relief="solid")
    e_koszt.pack(fill="x", ipady=3, pady=(2, 0))

    f_dz = tk.Frame(row_koszt, bg="#ffffff")
    f_dz.grid(row=0, column=1, sticky="ew")
    tk.Label(
        f_dz, text="DATA ZAŁATWIENIA *", font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#b91c1c"
    ).pack(anchor="w")
    e_data_zal = tk.Entry(f_dz, font=("Segoe UI", 10), bd=1, relief="solid")
    e_data_zal.pack(fill="x", ipady=3, pady=(2, 0))

    # PRZYCZYNA ZAISTNIENIA WADY/USTERKI
    tk.Label(
        card2_body, text="PRZYCZYNA ZAISTNIENIA WADY/USTERKI", font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#64748b"
    ).pack(anchor="w")
    txt_przyczyna = tk.Text(
        card2_body, font=("Segoe UI", 9), height=2, bd=1, relief="solid"
    )
    txt_przyczyna.pack(fill="x", pady=(2, 10))

    # SPOSÓB ZAŁATWIENIA / ROZWIĄZANIA SPRAWY (POLE TEKSTOWE - OPIS DZIAŁAŃ)
    tk.Label(
        card2_body,
        text="SPOSÓB ZAŁATWIENIA / ROZWIĄZANIA SPRAWY",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#64748b",
    ).pack(anchor="w")
    txt_sposob_opis = tk.Text(
        card2_body, font=("Segoe UI", 9), height=2, bd=1, relief="solid"
    )
    txt_sposob_opis.pack(fill="x", pady=(2, 2))

    tk.Label(
        card2_body,
        text="Opis podjętych działań naprawczych",
        font=("Segoe UI", 7, "italic"),
        bg="#ffffff",
        fg="#94a3b8",
    ).pack(anchor="w", pady=(0, 10))

    # DZIAŁANIA KORYGUJĄCE
    tk.Label(
        card2_body, text="CZY KONIECZNE DZIAŁANIA KORYGUJĄCE?", font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#64748b"
    ).pack(anchor="w")
    korygujace_var = tk.StringVar(value="TAK")

    f_kor_btn = tk.Frame(card2_body, bg="#ffffff")
    f_kor_btn.pack(anchor="w", pady=(3, 10))

    btn_kor_tak = tk.Button(
        f_kor_btn, text="TAK", font=("Segoe UI", 8, "bold"), bd=1, relief="solid", padx=14, pady=2
    )
    btn_kor_nie = tk.Button(
        f_kor_btn, text="NIE", font=("Segoe UI", 8, "bold"), bd=1, relief="solid", padx=14, pady=2
    )

    def ustaw_kor(val):
        korygujace_var.set(val)
        btn_kor_tak.config(
            bg="#1f4e5b" if val == "TAK" else "#ffffff",
            fg="white" if val == "TAK" else "#475569",
        )
        btn_kor_nie.config(
            bg="#1f4e5b" if val == "NIE" else "#ffffff",
            fg="white" if val == "NIE" else "#475569",
        )

    btn_kor_tak.config(command=lambda: ustaw_kor("TAK"))
    btn_kor_nie.config(command=lambda: ustaw_kor("NIE"))
    btn_kor_tak.pack(side="left", padx=(0, 5))
    btn_kor_nie.pack(side="left")

    tk.Label(
        card2_body, text="JAKIE DZIAŁANIA KORYGUJĄCE", font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#64748b"
    ).pack(anchor="w")
    txt_dzialania_kor = tk.Text(
        card2_body, font=("Segoe UI", 9), height=2, bd=1, relief="solid"
    )
    txt_dzialania_kor.pack(fill="x", pady=(2, 20))

    # ŁADOWANIE DANYCH DO FORMULARZA
    def wczytaj_reklamacje_do_panelu():
        nonlocal aktualna_reklamacja
        nr_szukany = e_szukaj_nr.get().strip().upper().replace("_", "/")

        dane = wczytajDane()
        znaleziona = None
        for r in dane:
            nr_db = r.get("nr_rek", "").strip().upper().replace("_", "/")
            if nr_db == nr_szukany:
                znaleziona = r
                break

        if not znaleziona:
            messagebox.showwarning(
                "Nie znaleziono",
                f"Nie odnaleziono w bazie reklamacji o numerze: {nr_szukany}",
            )
            aktualna_reklamacja = {}
            return

        aktualna_reklamacja = znaleziona

        status = znaleziona.get("status", "NOWE")
        lbl_status_badge.config(text=f" {status} ")

        odp = znaleziona.get(
            "odpowiedzialny",
            znaleziona.get("osoba_rejestrujaca", "Marek Zieliński"),
        )
        lbl_osoba_odp.config(text=f"Osoba odpowiedzialna: {odp}")
        combo_zalogowany.set(odp)

        # 1. Ładowanie decyzji przyciskowej (UZNANO / UZNANO CZĘŚCIOWO / NIE UZNANO)
        decyzja_val = znaleziona.get(
            "sposob_zalatwienia_decyzja",
            znaleziona.get("forma", "UZNANO CZĘŚCIOWO"),
        )
        if decyzja_val not in ["UZNANO", "UZNANO CZĘŚCIOWO", "UZNANO CZEŚCIOWO", "NIE UZNANO"]:
            decyzja_val = "UZNANO CZĘŚCIOWO"
        ustaw_sposob(decyzja_val)

        # 2. Ładowanie opisu tekstowego sposobu załatwienia do pola Text
        txt_sposob_opis.delete("1.0", "end")
        opis_val = znaleziona.get(
            "sposob_zalatwienia_opis", znaleziona.get("forma", "")
        )
        # Jeśli w polu 'forma' znajdował się tylko krótki status decyzji, nie wklejamy go do tekstu
        if opis_val in ["UZNANO", "UZNANO CZĘŚCIOWO", "UZNANO CZEŚCIOWO", "NIE UZNANO"]:
            opis_val = ""
        txt_sposob_opis.insert("1.0", opis_val)

        e_term_std.delete(0, "end")
        e_term_std.insert(0, znaleziona.get("termin_std", "04.08.2026"))

        e_term_akt.delete(0, "end")
        e_term_akt.insert(0, znaleziona.get("termin_akt", "11.08.2026"))

        txt_uzasadnienie.delete("1.0", "end")
        uzasadnienie_val = znaleziona.get("uzasadnienie", "").strip()
        txt_uzasadnienie.insert("1.0", uzasadnienie_val)

        if uzasadnienie_val:
            wydluzenie_var.set(True)
            f_termDateTime.pack(fill="x", pady=(5, 0))
        else:
            wydluzenie_var.set(False)
            f_termDateTime.pack_forget()

        ustaw_podw(znaleziona.get("czy_podwykonawca", "TAK"))

        e_podwykonawca.delete(0, "end")
        e_podwykonawca.insert(0, znaleziona.get("podwykonawca", ""))

        e_koszt.delete(0, "end")
        e_koszt.insert(0, str(znaleziona.get("koszty", "")))

        e_data_zal.delete(0, "end")
        e_data_zal.insert(0, znaleziona.get("data_zak", ""))

        txt_przyczyna.delete("1.0", "end")
        txt_przyczyna.insert("1.0", znaleziona.get("przyczyna", ""))

        ustaw_kor(znaleziona.get("czy_korygujace", "TAK"))

        txt_dzialania_kor.delete("1.0", "end")
        txt_dzialania_kor.insert(
            "1.0", znaleziona.get("dzialania_korygujace", "")
        )

    btn_laduj.config(command=wczytaj_reklamacje_do_panelu)

    # ZAPIS I PRZEKAZANIE DO ZAMKNIĘCIA
    # ZAPIS I AUTOMATYCZNE ZAMKNIĘCIE REKLAMACJI
    def zapisz_i_zakoncz():
        if not aktualna_reklamacja:
            messagebox.showwarning(
                "Brak danych",
                "Wpisz numer reklamacji i kliknij '🔍 Wczytaj' przed zapisem!",
            )
            return

        nr_szukany = e_szukaj_nr.get().strip().upper().replace("_", "/")
        dane_wszystkie = wczytajDane()
        zmieniono = False

        for r in dane_wszystkie:
            nr_db = r.get("nr_rek", "").strip().upper().replace("_", "/")
            if nr_db == nr_szukany:
                opis_sposobu = txt_sposob_opis.get("1.0", "end-1c").strip()
                decyzja_sposob = sposob_var.get()

                # Zapisujemy sposób załatwienia
                r["forma"] = opis_sposobu if opis_sposobu else decyzja_sposob
                r["sposob_zalatwienia_decyzja"] = decyzja_sposob
                r["sposob_zalatwienia_opis"] = opis_sposobu

                r["termin_std"] = e_term_std.get()
                r["termin_akt"] = (
                    e_term_akt.get() if wydluzenie_var.get() else ""
                )
                r["uzasadnienie"] = (
                    txt_uzasadnienie.get("1.0", "end-1c")
                    if wydluzenie_var.get()
                    else ""
                )
                r["czy_podwykonawca"] = podwykonawca_var.get()
                r["podwykonawca"] = e_podwykonawca.get()
                r["koszty"] = e_koszt.get()
                r["data_zak"] = e_data_zal.get()
                r["przyczyna"] = txt_przyczyna.get("1.0", "end-1c")
                r["czy_korygujace"] = korygujace_var.get()
                r["dzialania_korygujace"] = txt_dzialania_kor.get(
                    "1.0", "end-1c"
                )

                # AUTOMATYCZNE ZAMKNIĘCIE REKLAMACJI
                # Możesz wybrać: "ZAMKNIĘTE" lub uzależnić status od decyzji:
                if decyzja_sposob in ["UZNANO", "UZNANO CZĘŚCIOWO"]:
                    r["status"] = "UZNANE GWARANCYJNIE"
                elif decyzja_sposob == "NIE UZNANO":
                    r["status"] = "NIEUZNANE GWARANCYJNIE"
                else:
                    r["status"] = "ZAMKNIĘTE"

                zmieniono = True

                # Regeneracja PDF oraz pojedynczego pliku JSON w folderze Reklamacje_Dane
                try:
                    folder_projektu = os.path.dirname(
                        os.path.abspath(__file__)
                    )
                    nazwa_folderu = nr_db.replace("/", "_")
                    folder_docelowy = os.path.join(
                        folder_projektu, "Reklamacje_Dane", nazwa_folderu
                    )

                    if os.path.exists(folder_docelowy):
                        generujPdf(folder_docelowy, r, nr_db, folder_projektu)
                        generujJSON(
                            folder_docelowy, r, nazwa_folderu, folder_projektu
                        )
                        print(
                            f"[PANEL PRACOWNIKA] Zaktualizowano i zamknięto pliki w: {nazwa_folderu}"
                        )
                except Exception as ex:
                    print(f"[BŁĄD GENEROWANIA PLIKÓW]: {ex}")

                break

        if zmieniono:
            zapiszDane(dane_wszystkie)
            messagebox.showinfo(
                "Sukces",
                f"Zgłoszenie {nr_szukany} zostało pomyślnie zakończone i zamknięte!",
            )
            if odswiez_callback:
                odswiez_callback()
            win.destroy()

            
    btn_finish = tk.Button(
        card2_body,
        text="✉ Wyślij (zakończ zgłoszenie)",
        font=("Segoe UI", 10, "bold"),
        bg="#1f4e5b",
        fg="white",
        activebackground="#2d6a78",
        activeforeground="white",
        bd=0,
        padx=18,
        pady=9,
        cursor="hand2",
        command=zapisz_i_zakoncz,
    )
    btn_finish.pack(anchor="w", pady=(0, 10))

    wczytaj_reklamacje_do_panelu()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Testowanie widoku")

    otworzPanelRealizacji(root, "ZG/2026/001")

    root.mainloop()