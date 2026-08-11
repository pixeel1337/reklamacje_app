import tkinter as tk
from tkinter import ttk

def otworzPanelRealizacji(parent_window):
    win = tk.Toplevel(parent_window)
    win.title("Realizacja zgłoszenia - ZG/2026/01")
    win.geometry("780x920")
    win.configure(bg="#f4f1ea")

    win.transient(parent_window)
    win.grab_set()


    # TOP BAR
    top_bar = tk.Frame(win, bg="#f4f1ea", padx=20, pady=20)
    top_bar.pack(fill="x")

    btn_back = tk.Button(
        top_bar,
        text="← Wróć do rejestru",
        font=("Segoe UI", 10, "bold"),
        bg="#f4f1ea",
        fg="#1f4e5b",
        bd=0,
        cursor="hand2",
        command=win.destroy
    )
    btn_back.pack(side="left")

    nr_badge_frame = tk.Frame(top_bar, bg="#f4f1ea")
    nr_badge_frame.pack(side="right")

    lbl_nr = tk.Label(
        nr_badge_frame,
        text=" W TRAKCIE ",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#d97706",
        relief="solid",
        bd=1
    )
    lbl_nr.pack(side="left", padx=(0, 5))

    lbl_status = tk.Label(
        nr_badge_frame,
        text=" W TRAKCIE ",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#d97706",
        relief="solid",
        bd=1
    )
    lbl_status.pack(side="left")


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



    # Kafelek: Rola i użytkownik

    sec1_card = tk.Frame(scroll_frame, bg="#f8f6f0", padx=15, pady=12)
    sec1_card.pack(fill="x", pady=(0, 15))

    card1_body = tk.Frame(sec1_card, bg="#f8f6f0", padx=15, pady=12)
    card1_body.pack(fill="x")

    card1_body.columnconfigure(0, weight=1)
    card1_body.columnconfigure(1, weight=1)

    # Pracujesz jako
    f_rola = tk.Frame(card1_body, bg="#f8f6f0")
    f_rola.grid(row=0, column=0, sticky="ew", padx=(0, 10))
    tk.Label(
        f_rola,
        text="PRACUJESZ JAKO",
        font=("Segoe UI", 8, "bold"),
        bg="#f8f6f0",
        fg="#64748b"
    ).pack(anchor="w")

    combo_pracujesz = ttk.Combobox(
        f_rola, 
        values=["Osoba odpowiedzialna"],
        state="readonly",
        font=("Segoe UI", 10)
    )
    combo_pracujesz.set("Osoba odpowiedzialna")
    combo_pracujesz.pack(fill="x", pady=(3, 0), ipady=2)

    # Zalogowany jako
    f_zalogowany = tk.Frame(card1_body, bg="#f8f6f0")
    f_zalogowany.grid(row=0, column=1, sticky="ew")
    tk.Label(
        f_zalogowany,
        text="ZALOGOWANY JAKO (OSOBA ODPOWIEDZIALNA)",
        font=("Segoe UI", 8, "bold"),
        bg="#f8f6f0",
        fg="#64748b"
    ).pack(anchor="w")

    combo_zalogowany = ttk.Combobox(
        f_zalogowany,
        values=["Marek Zieliński"],
        state="readonly",
        font=("Segoe UI", 10)
    )
    combo_zalogowany.set("Marek Zieliński")
    combo_zalogowany.pack(fill="x", pady=(3, 0), ipady=2)


    # Kafelek: Realizacja i zamknięcie
    sec2_card = tk.Frame(scroll_frame, bg="#ffffff", bd=1, relief="solid")
    sec2_card.pack(fill="x", pady=(0, 20))

    card2_body = tk.Frame(sec2_card, bg="#ffffff", padx=20, pady=15)
    card2_body.pack(fill="x")

    sec2_title = tk.Label(
        card2_body,
        text="⚙ 3 · REALIZACJA I ZAMKNIĘCIE",
        font=("Segoe UI", 11, "bold"),
        bg="#ffffff",
        fg="#0f172a"
    )
    sec2_title.pack(anchor="w", pady=(0, 10))

    lbl_osoba_odp = tk.Label(
        card2_body,
        text="Osoba odpowiedzialna: Marek Zieliński",
        font=("Segoe UI", 9, "bold"),
        bg="#ffffff",
        fg="#0f172a",
    )
    lbl_osoba_odp.pack(anchor="w", pady=(0, 15))

    tk.Label(
        card2_body,
        text="SPOSÓB ZAŁATWIENIA SPRAWY *",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#b91c1c"
    ).pack(anchor="w")

    sposob_var = tk.StringVar(value="UZNANO CZEŚCIOWO")

    f_sposob_btn = tk.Frame(card2_body, bg="#ffffff")
    f_sposob_btn.pack(anchor="w", pady=(5, 15))

    btn_uznano = tk.Button(
        f_sposob_btn,
        text="UZNANO",
        font=("Segoe UI", 8, "bold"),
        bd=1,
        relief="solid",
        padx=12,
        pady=4
    )

    btn_czesciowo = tk.Button(
        f_sposob_btn,
        text="UZNANO CZĘŚCIOWO",
        font=("Segoe UI", 8, "bold"),
        bd=1,
        relief="solid",
        padx=12,
        pady=4
    )

    btn_nieuznano = tk.Button(
        f_sposob_btn,
        text="NIE UZNANO",
        font=("Segoe UI", 8, "bold"),
        bd=1,
        relief="solid",
        padx=12,
        pady=4
    )

    def ustaw_sposob(val):
        sposob_var.set(val)
        btn_uznano.config(
            bg="#a51d24" if val == "UZNANO" else "#ffffff",
            fg="white" if val == "UZNANO" else "#475569"
        )
        btn_czesciowo.config(
            bg="#a51d24" if val == "UZNANO CZĘŚCIOWO" else "#ffffff",
            fg="white" if val == "UZNANO CZĘŚCIOWO" else "#475569"
        )
        btn_nieuznano.config(
            bg="#a51d24" if val == "NIE UZNANO" else "#ffffff",
            fg="white" if val == "NIE UZNANO" else "#475569"
        )

    btn_uznano.config(command=lambda: ustaw_sposob("UZNANO"))
    btn_czesciowo.config(command=lambda: ustaw_sposob("UZNANO CZEŚCIOWO"))
    btn_nieuznano.config(command=lambda: ustaw_sposob("NIE UZNANO"))

    btn_uznano.pack(side="left", padx=(0, 15))
    btn_czesciowo.pack(side="left", padx=(0, 15))
    btn_nieuznano.pack(side="left")

    ustaw_sposob("UZNANO CZEŚCIOWO")

    # Sekcja terminów

    f_termDateTime = tk.Frame(
        card2_body, bg="#f8fafc", bd=1, relief="solid", padx=12, pady=12
    )
    f_termDateTime.pack(fill="x", pady=(0, 15))

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
    e_term_std.insert(0, "04.08.2026")
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
    e_term_akt.insert(0, "11.08.2026")
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
    txt_uzasadnienie.insert(
        "1.0",
        "Oczekiwanie na dostawę zamiennika złącza od dostawcy — przewidywany"
        " czas dostawy 7 dni.",
    )
    txt_uzasadnienie.pack(fill="x", pady=(2, 0))


    tk.Label(
        card2_body,
        text="Czy dotyczy podwykonawcy",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#64748b"
    ).pack(anchor="w")
    podwykonawca_var = tk.StringVar(value="TAK")

    f_podw_btn = tk.Frame(card2_body, bg="#ffffff")
    f_podw_btn.pack(anchor="w", pady=(3, 10))

    btn_podw_tak = tk.Button(
        f_podw_btn,
        text="TAK",
        font=("Segoe UI", 8, "bold"),
        bd=1,
        relief="solid",
        padx=14,
        pady=2,
    )
    btn_podw_nie = tk.Button(
        f_podw_btn,
        text="NIE",
        font=("Segoe UI", 8, "bold"),
        bd=1,
        relief="solid",
        padx=14,
        pady=2,
    )

    def ustaw_podw(val):
        podwykonawca_var.set(val)
        btn_podw_tak.config(
            bg="#1f4e5b" if val == "TAK" else "#ffffff",
            fg="white" if val == "NIE" else "#475569"
        )
        btn_podw_nie.config(
            bg="#1f4e5b" if val == "NIE" else "#ffffff",
            fg="white" if val == "NIE" else "#475569"
        )

    btn_podw_tak.config(command=lambda: ustaw_podw("TAK"))
    btn_podw_nie.config(command=lambda: ustaw_podw("NIE"))
    btn_podw_tak.pack(side="left", padx=(0, 5))
    btn_podw_nie.pack(side="left")

    ustaw_podw("TAK")

    tk.Label(
        card2_body,
        text="NAZWA PODWYKONAWCY",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#64748b"
    ).pack(anchor="w")
    e_podwykonawca = tk.Entry(card2_body, font=("Segoe UI", 10), bd=1, relief="solid")
    e_podwykonawca.insert(0, "Instal-Mont Sp. z o. o.")
    e_podwykonawca.pack(fill="x", ipady=3, pady=(2, 10))


    # Koszty + Data załatwienia
    row_koszt = tk.Frame(card2_body, bg="#ffffff")
    row_koszt.pack(fill="x", pady=(0, 10))
    row_koszt.columnconfigure(0, weight=0)
    row_koszt.columnconfigure(1, weight=1)

    f_k = tk.Frame(row_koszt, bg="#ffffff")
    f_k.grid(row=0, column=0, sticky="ew", padx=(0, 10))
    tk.Label(
        f_k,
        text="KOSZTY NAPRAWY (ZŁ)",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#64748b",
    ).pack(anchor="w")
    e_koszt = tk.Entry(f_k, font=("Segoe UI", 10), bd=1, relief="solid")
    e_koszt.insert(0, "4 850, 00")
    e_koszt.pack(fill="x", ipady=3, pady=(2, 0))

    f_dz = tk.Frame(row_koszt, bg="#ffffff")
    f_dz.grid(row=0, column=1, sticky="ew")
    tk.Label(
        f_dz,
        text="DATA ZAŁATWIENIA *",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#b91c1c",
    ).pack(anchor="w")
    e_data_zal = tk.Entry(f_dz, font=("Segoe UI", 10), bd=1, relief="solid")
    e_data_zal.insert(0, "12.08.2026")
    e_data_zal.pack(fill="x", ipady=3, pady=(2, 0))


    # Przyczyna Label
    tk.Label(
        card2_body,
        text="PRZYCZYNA ZAISTNIENIA WADY/USTERKI",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#64748b",
    ).pack(anchor="w")
    txt_przyczyna = tk.Text(
        card2_body, font=("Segoe UI", 9), height=2, bd=1, relief="solid"
    )
    txt_przyczyna.insert(
        "1.0",
        "Korozja złącza spowodowana niewłaściwym doborem uszczelnienia na etapie"
        " montażu.",
    )
    txt_przyczyna.pack(fill="x", pady=(2, 10))

    # Sposób załatwienia
    tk.Label(
        card2_body,
        text="PRZYCZYNA ZAISTNIENIA WADY/USTERKI",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#64748b",
    ).pack(anchor="w")
    txt_przyczyna = tk.Text(
        card2_body, font=("Segoe UI", 9), height=2, bd=1, relief="solid"
    )
    txt_przyczyna.insert(
        "1.0",
        "Korozja złącza spowodowana niewłaściwym doborem uszczelnienia na etapie"
        " montażu.",
    )
    txt_przyczyna.pack(fill="x", pady=(2, 10))

    # Czy konieczne działanie korygujące
    tk.Label(
        card2_body,
        text="CZY KONIECZNE DZIAŁANIA KORYGUJĄCE?",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#64748b",
    ).pack(anchor="w")
    korygujace_var = tk.StringVar(value="TAK")

    f_kor_btn = tk.Frame(card2_body, bg="#ffffff")
    f_kor_btn.pack(anchor="w", pady=(3, 10))

    btn_kor_tak = tk.Button(
        f_kor_btn,
        text="TAK",
        font=("Segoe UI", 8, "bold"),
        bd=1,
        relief="solid",
        padx=14,
        pady=2,
    )
    btn_kor_nie = tk.Button(
        f_kor_btn,
        text="NIE",
        font=("Segoe UI", 8, "bold"),
        bd=1,
        relief="solid",
        padx=14,
        pady=2,
    )


    def ustaw_kor(val):
        korygujace_var.set(val)
        btn_kor_tak.config(
            bg="#1f4e5b" if val == "TAK" else "#ffffff",
            fg="white" if val == "TAK" else "#475569"
        )
        btn_kor_nie.config(
            bg="#1f4e5b" if val == "NIE" else "#ffffff",
            fg="white" if val == "NIE" else "#475569"
        )

    btn_kor_tak.config(command=lambda: ustaw_kor("TAK"))
    btn_kor_nie.config(command=lambda: ustaw_kor("NIE"))
    btn_kor_tak.pack(side="left", padx=(0, 5))
    btn_kor_nie.pack(side="left")

    ustaw_kor("TAK")

    tk.Label(
        card2_body,
        text="JAKIE DZIAŁANIA KORYGUJĄCE",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#64748b",
    ).pack(anchor="w")
    txt_dzialania_kor = tk.Text(
        card2_body, font=("Segoe UI", 9), height=2, bd=1, relief="solid"
    )
    txt_dzialania_kor.insert(
        "1.0",
        "Aktualizacja specyfikacji uszczelek dla złączy tego typu we wszystkich"
        " projektach w realizacji.",
    )
    txt_dzialania_kor.pack(fill="x", pady=(2, 20))

    # Przycisk zapisu
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
        cursor="hand2"
    )
    btn_finish.pack(anchor="w", pady=(0, 10))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Testowanie widoku")
    
    label = tk.Label(root, text="Okno główne w tle (nie zamykaj)")
    label.pack(expand=True)

    otworzPanelRealizacji(root)

    root.mainloop()




