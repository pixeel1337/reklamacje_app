import tkinter as tk
from tkinter import messagebox, ttk

from baza import aktualizujReklamacje, wczytajDane
from formularz import otworzFormularzDodawania


def odswiezWszystko(
    tree,
    sub_lbl,
    kpi_labels,
    btn_all,
    btn_open,
    szukana_fraza="",
    tylko_otwarte=False,
):
    for item in tree.get_children():
        tree.delete(item)

    dane = wczytajDane()

    total_count = len(dane)
    open_count = sum(
        1
        for r in dane
        if r.get("status")
        in [
            "NOWE",
            "W TRAKCIE",
            "CZEKA NA ZAMKNIĘCIE",
            "PRZEKAZANE DO REALIZACJI",
        ]
    )
    sys_count = sum(
        1 for r in dane if r.get("typ_niezgodnosci") == "Systemowa"
    )
    uznane_count = sum(
        1 for r in dane if r.get("status") == "UZNANE GWARANCYJNIE"
    )
    nieuznane_count = sum(
        1 for r in dane if r.get("status") in ["NIEUZNANE GWARANCYJNIE", "ODRZUCONE"]
    )

    sub_lbl.config(text=f"{open_count} zgłoszeń aktywnych")

    kpi_labels[0].config(text=str(open_count))
    kpi_labels[1].config(text=str(sys_count))
    kpi_labels[2].config(text=str(uznane_count))
    kpi_labels[3].config(text=str(nieuznane_count))

    btn_all.config(text=f"Cały rejestr ({total_count})")
    btn_open.config(text=f"Otwarte zgłoszenia ({open_count})")

    fraza = szukana_fraza.lower().strip()

    for r in dane:
        status = r.get("status", "NOWE")
        if tylko_otwarte and status not in [
            "NOWE",
            "W TRAKCIE",
            "CZEKA NA ZAMKNIĘCIE",
            "PRZEKAZANE DO REALIZACJI",
        ]:
            continue

        nr_rek = r.get("nr_rek", "")
        klient = r.get("klient", "")
        nr_zadania = r.get("nr_zadania") or r.get("nr_projektu", "")
        nazwa_zadania = r.get("nazwa_zadania", "")
        odpowiedzialny = r.get("odpowiedzialny") or r.get("osoba_rejestrujaca", "")
        opis = r.get("opis", "")

        if fraza:
            dopasowanie = (
                fraza in nr_rek.lower()
                or fraza in klient.lower()
                or fraza in nr_zadania.lower()
                or fraza in nazwa_zadania.lower()
                or fraza in odpowiedzialny.lower()
                or fraza in opis.lower()
                or fraza in status.lower()
            )
            if not dopasowanie:
                continue

        wiersz = (
            f"#{r.get('id', 0):03d}",
            nr_rek if nr_rek else "—",
            r.get("data_zgl", "—"),
            klient if klient else "—",
            nr_zadania if nr_zadania else "—",
            nazwa_zadania if nazwa_zadania else "—",
            r.get("forma", "—"),
            odpowiedzialny if odpowiedzialny else "—",
            r.get("data_zak", "—"),
            status,
            r.get("typ_niezgodnosci", "—"),
            opis if opis else "—",
        )
        tree.insert("", "end", values=wiersz)


def zmienStatusZaznaczonego(tree, nowy_status, odswiez_callback):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Brak wyboru", "Zaznacz zgłoszenie z listy!")
        return

    item_values = tree.item(selected_item[0], "values")
    nr_rek = item_values[1]

    wynik = aktualizujReklamacje(nr_rek, {"status": nowy_status}, regeneruj_pliki=True)
    if wynik:
        messagebox.showinfo(
            "Sukces", f"Zmieniono status zgłoszenia {nr_rek} na: {nowy_status}"
        )
        odswiez_callback()
    else:
        messagebox.showerror("Błąd", f"Nie udało się zmienić statusu dla {nr_rek}.")


def stworzRejestrZgloszen():
    root = tk.Tk()
    root.title("System Obsługi Reklamacji")
    root.geometry("1350x780")
    root.configure(bg="#eef2f5")

    filtr_tylko_otwarte = tk.BooleanVar(value=False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Custom.Treeview",
        background="#ffffff",
        foreground="#1e293b",
        rowheight=32,
        fieldbackground="#ffffff",
        font=("Segoe UI", 9),
    )
    style.configure(
        "Custom.Treeview.Heading",
        background="#f8fafc",
        foreground="#475569",
        font=("Segoe UI", 8, "bold"),
        relief="flat",
    )

    # --- NAGŁÓWEK ---
    header_frame = tk.Frame(root, bg="#eef2f5", padx=20, pady=15)
    header_frame.pack(fill="x")

    title_box = tk.Frame(header_frame, bg="#eef2f5")
    title_box.pack(side="left")

    title_lbl = tk.Label(
        title_box,
        text="Rejestr Zgłoszeń Reklamacyjnych",
        font=("Segoe UI", 16, "bold"),
        bg="#eef2f5",
        fg="#0f172a",
    )
    title_lbl.pack(anchor="w")

    sub_lbl = tk.Label(
        title_box,
        text="0 zgłoszeń aktywnych",
        font=("Segoe UI", 9),
        bg="#eef2f5",
        fg="#64748b",
    )
    sub_lbl.pack(anchor="w")

    def wywolaj_odswiezanie():
        odswiezWszystko(
            tree,
            sub_lbl,
            kpi_labels,
            btn_all,
            btn_open,
            entry_search.get(),
            filtr_tylko_otwarte.get(),
        )

    btn_add = tk.Button(
        header_frame,
        text="+ Dodaj nowe zgłoszenie",
        font=("Segoe UI", 9, "bold"),
        bg="#1f4e5b",
        fg="white",
        activebackground="#2d6a78",
        activeforeground="white",
        bd=0,
        padx=16,
        pady=8,
        cursor="hand2",
        command=lambda: otworzFormularzDodawania(root, wywolaj_odswiezanie),
    )
    btn_add.pack(side="right")

    # --- KAFELKI KPI ---
    kpi_frame = tk.Frame(root, bg="#eef2f5", padx=20)
    kpi_frame.pack(fill="x", pady=(0, 15))

    cards_data = [
        ("CZEKA NA ZAMKNIĘCIE", "otwarte zgłoszenia", "#d97706"),
        ("ZGŁOSZENIA SYSTEMOWE", "typ systemowy", "#475569"),
        ("UZNANE GWARANCYJNIE", "decyzja pozytywna", "#16a34a"),
        ("NIEUZNANE / ODRZUCONE", "decyzja negatywna", "#dc2626"),
    ]

    kpi_labels = []
    for i, (title, desc, color) in enumerate(cards_data):
        kpi_frame.columnconfigure(i, weight=1, uniform="kpi")
        card = tk.Frame(kpi_frame, bg=color)
        card.grid(row=0, column=i, padx=5, sticky="ew")

        bar = tk.Frame(card, bg=color, height=4)
        bar.pack(fill="x", side="top")

        body = tk.Frame(card, bg="#ffffff", padx=12, pady=10)
        body.pack(fill="both", expand=True)

        tk.Label(
            body,
            text=title,
            font=("Segoe UI", 7, "bold"),
            bg="#ffffff",
            fg="#475569",
            anchor="w",
        ).pack(anchor="w")

        val_lbl = tk.Label(
            body,
            text="0",
            font=("Segoe UI", 18, "bold"),
            bg="#ffffff",
            fg="#0f172a",
            anchor="w",
        )
        val_lbl.pack(anchor="w", pady=(2, 2))
        kpi_labels.append(val_lbl)

        tk.Label(
            body,
            text=desc,
            font=("Segoe UI", 7),
            bg="#ffffff",
            fg="#64748b",
            anchor="w",
        ).pack(anchor="w")

    # --- PASEK NARZĘDZI ---
    toolbar = tk.Frame(root, bg="#eef2f5", padx=20)
    toolbar.pack(fill="x", pady=(0, 10))

    tabs_frame = tk.Frame(toolbar, bg="#eef2f5")
    tabs_frame.pack(side="left")

    def przelacz_filtr(tylko_otw):
        filtr_tylko_otwarte.set(tylko_otw)
        btn_all.config(
            bg="#1f4e5b" if not tylko_otw else "#ffffff",
            fg="white" if not tylko_otw else "#475569",
            bd=0 if not tylko_otw else 1,
        )
        btn_open.config(
            bg="#1f4e5b" if tylko_otw else "#ffffff",
            fg="white" if tylko_otw else "#475569",
            bd=0 if tylko_otw else 1,
        )
        wywolaj_odswiezanie()

    btn_all = tk.Button(
        tabs_frame,
        text="Cały rejestr (0)",
        font=("Segoe UI", 9, "bold"),
        bg="#1f4e5b",
        fg="white",
        bd=0,
        padx=14,
        pady=6,
        cursor="hand2",
        command=lambda: przelacz_filtr(False),
    )
    btn_all.pack(side="left", padx=(0, 6))

    btn_open = tk.Button(
        tabs_frame,
        text="Otwarte zgłoszenia (0)",
        font=("Segoe UI", 9, "bold"),
        bg="#ffffff",
        fg="#475569",
        bd=1,
        relief="solid",
        highlightthickness=0,
        padx=14,
        pady=5,
        cursor="hand2",
        command=lambda: przelacz_filtr(True),
    )
    btn_open.pack(side="left", padx=(0, 15))

    btn_accept_gui = tk.Button(
        tabs_frame,
        text="✓ Akceptuj zaznaczone",
        font=("Segoe UI", 8, "bold"),
        bg="#16a34a",
        fg="white",
        bd=0,
        padx=10,
        pady=5,
        cursor="hand2",
        command=lambda: zmienStatusZaznaczonego(
            tree, "PRZEKAZANE DO REALIZACJI", wywolaj_odswiezanie
        ),
    )
    btn_accept_gui.pack(side="left", padx=(0, 5))

    btn_reject_gui = tk.Button(
        tabs_frame,
        text="✕ Odrzuć zaznaczone",
        font=("Segoe UI", 8, "bold"),
        bg="#dc2626",
        fg="white",
        bd=0,
        padx=10,
        pady=5,
        cursor="hand2",
        command=lambda: zmienStatusZaznaczonego(
            tree, "ODRZUCONE", wywolaj_odswiezanie
        ),
    )
    btn_reject_gui.pack(side="left")

    search_frame = tk.Frame(toolbar, bg="#ffffff", bd=1, relief="solid")
    search_frame.pack(side="right")

    tk.Label(
        search_frame, text="🔍", font=("Segoe UI", 9), bg="#ffffff", fg="#64748b", padx=6
    ).pack(side="left")

    entry_search = tk.Entry(
        search_frame, font=("Segoe UI", 9), bd=0, bg="#ffffff", fg="#0f172a", width=25
    )
    entry_search.pack(side="left", ipady=4, padx=(0, 6))
    entry_search.bind("<KeyRelease>", lambda event: wywolaj_odswiezanie())

    # --- TABELA Z DANYMI ---
    table_container = tk.Frame(root, bg="#ffffff")
    table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    columns = (
        "lp",
        "nr_rek",
        "data_zgl",
        "klient",
        "nr_zadania",
        "nazwa_zadania",
        "forma",
        "odpowiedzialny",
        "data_zak",
        "status",
        "typ_niezgodnosci",
        "opis_przyczyny",
    )

    tree = ttk.Treeview(
        table_container,
        columns=columns,
        show="headings",
        style="Custom.Treeview",
    )

    headings = [
        ("lp", "LP", 45, "center"),
        ("nr_rek", "NR REKLAMACJI", 110, "center"),
        ("data_zgl", "DATA ZGŁ.", 85, "center"),
        ("klient", "KLIENT", 120, "w"),
        ("nr_zadania", "NR ZADANIA", 90, "center"),
        ("nazwa_zadania", "NAZWA ZADANIA", 140, "w"),
        ("forma", "FORMA ZAŁATWIENIA", 120, "w"),
        ("odpowiedzialny", "ODPOWIEDZIALNY", 120, "w"),
        ("data_zak", "DATA ZAK.", 85, "center"),
        ("status", "STATUS", 130, "w"),
        ("typ_niezgodnosci", "TYP NIEZGODNOŚCI", 120, "w"),
        ("opis_przyczyny", "OPIS PRZYCZYNY", 160, "w"),
    ]

    for col_id, text, width, align in headings:
        tree.heading(col_id, text=text)
        tree.column(col_id, width=width, anchor=align)

    vsb = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(table_container, orient="horizontal", command=tree.xview)
    tree.configure(yscroll=vsb.set, xscroll=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    table_container.grid_rowconfigure(0, weight=1)
    table_container.grid_columnconfigure(0, weight=1)

    wywolaj_odswiezanie()
    root.mainloop()


if __name__ == "__main__":
    stworzRejestrZgloszen()