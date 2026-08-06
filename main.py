import tkinter as tk
from tkinter import messagebox, ttk
from formularz import otworzFormularzDodawania
from baza import wczytajDane


def odswiezTabele(tree):
    for item in tree.get_children():
        tree.delete(item)

    dane = wczytajDane()
    for r in dane:
        wiersz = (
            f"#{r.get('id', 0):03d}",
            r.get("nr_rek", "—"),
            r.get("data_zgl", "—"),
            r.get("klient", "—"),
            r.get("nr_projektu", "—"),
            r.get("nazwa_zadania", "—"),
            r.get("forma", "—"),
            r.get("odpowiedzialny", "—"),
            r.get("data_zak", "—"),
            r.get("uwagi", "—"),
            r.get("typ_niezgodnosci", "—"),
            r.get("opis", "—"),
        )
        tree.insert("", "end", values=wiersz)


def stworzRejestrZgloszen():
    root = tk.Tk()
    root.title("Proces Reklamacyjny")
    root.geometry("1300x750")
    root.configure(bg="#eef2f5")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview",
                    background="#ffffff",
                    foreground="#1e293b",
                    rowheight=32,
                    fieldbackground="#ffffff",
                    font=("Segoe UI", 9))
    style.configure("Custom.Treeview.Heading",
                    background="#f8fafc",
                    foreground="#475569",
                    font=("Segoe UI", 8, "bold"),
                    relief="flat")
    style.map("Custom.Treeview",
              background=[("selected", "#cbd5e1")],
              foreground=[("selected", "#0f172a")])


    header_frame = tk.Frame(root, bg="#eef2f5", padx=20, pady=15)
    header_frame.pack(fill="x")

    title_box = tk.Frame(header_frame, bg="#eef2f5")
    title_box.pack(side="left")

    title_lbl = tk.Label(title_box, text="Rejestr Zgłoszeń Reklamacyjnych", font=("Segoe UI", 16, "bold"), bg="#eef2f5", fg="#0f172a")
    title_lbl.pack(anchor="w")

    sub_lbl = tk.Label(title_box, text="7 zgłoszeń aktywnych", font=("Segoe UI", 9), bg="#eef2f5", fg="#64748b")
    sub_lbl.pack(anchor="w")

    btn_add = tk.Button(header_frame, text="+ Dodaj nowe zgłoszenie", font=("Segoe UI", 9, "bold"), bg="#1f4e5b", fg="white",
                    activebackground="#2d6a78", activeforeground="white",
                    bd=0, padx=16, pady=8, cursor="hand2", 
                    command=lambda: otworzFormularzDodawania(root, lambda: odswiezTabele(tree)))
    btn_add.pack(side="right")

    kpi_frame = tk.Frame(root, bg="#eef2f5", padx=20)
    kpi_frame.pack(fill="x", pady=(0, 15))

    cards_data = [
        ("CZEKA NA ZAMKNIĘCIE", "3", "wszystkie otwarte, bez względu na rok", "#d97706"),
        ("ZGŁOSZENIA SYSTEMOWE (2026)", "2", "niezgodność typu systemowego", "#475569"),
        ("UZNANE GWARANCYJNIE (2026)", "2", "zamknięte z decyzją pozytywną", "#16a34a"),
        ("NIEUZNANE GWARANCYJNIE (2026)", "1", "zamknięte z decyzją negatywną", "#dc2626"),
    ]


    for i, (title, val, desc, color) in enumerate(cards_data):
        kpi_frame.columnconfigure(i, weight=1, uniform="kpi")

        card = tk.Frame(kpi_frame, bg=color, height=4)
        card.grid(row=0, column=i, padx=5, sticky="ew")

        bar = tk.Frame(card, bg=color, height=4)
        bar.pack(fill="x", side="top")

        body = tk.Frame(card, bg="#ffffff", padx=12, pady=10)
        body.pack(fill="both", expand=True)

        tk.Label(body, text=title, font=("Segoe UI", 7, "bold"), bg="#ffffff", fg="#475569", anchor="w").pack(anchor="w")
        tk.Label(body, text=val, font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#0f172a", anchor="w").pack(anchor="w", pady=(2, 2))
        tk.Label(body, text=desc, font=("Segoe UI", 7), bg="#ffffff", fg="#64748b", anchor="w").pack(anchor="w")


    toolbar = tk.Frame(root, bg="#eef2f5")
    toolbar.pack(fill="x", pady=(0, 10))

    tabs_frame = tk.Frame(toolbar, bg="#eef2f5")
    tabs_frame.pack(side="left")

    btn_all = tk.Button(tabs_frame, text="Cały rejestr (7)", font=("Segoe UI", 9, "bold"),
                        bg="#1f4e5b", fg="white", bd=0, padx=14, pady=6)
    btn_all.pack(side="left", padx=(0, 6))

    btn_open = tk.Button(tabs_frame, text="Otwarte zgłoszenia (3)", font=("Segoe UI", 9, "bold"),
                         bg="#ffffff", fg="#475569", bd=1, relief="solid", highlightthickness=0, padx=14, pady=5)
    btn_open.pack(side="left")

    search_frame = tk.Frame(toolbar, bg="#eef2f5")
    search_frame.pack(side="right")

    search_entry = tk.Entry(search_frame, font=("Segoe UI", 9), width=35, relief="solid", bd=1, fg="#64748b")
    search_entry.insert(0, "Szukaj: klient, nr reklamacji, nr zadania...")
    search_entry.pack(side="right")


    table_container = tk.Frame(root, bg="#ffffff")
    table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    columns = (
        "lp", "nr_rek", "data_zgl", "klient", "nr_zadania", 
        "nazwa_zadania", "forma", "odpowiedzialny", "data_zak", 
        "uwagi", "typ_niezgodnosci", "opis_przyczyny"
    )

    tree = ttk.Treeview(table_container, columns=columns, show="headings", style="Custom.Treeview")


    headings = [
        ("lp", "LP", 45, "center"),
        ("nr_rek", "NR REKLAMACJI", 110, "center"),
        ("data_zgl", "DATA ZGŁ.", 85, "center"),
        ("klient", "KLIENT", 120, "w"),
        ("nr_zadania", "NR ZADANIA", 90, "center"),
        ("nazwa_zadania", "NAZWA ZADANIA", 140, "w"),
        ("forma", "FORMA ZAŁATWIENIA", 110, "w"),
        ("odpowiedzialny", "ODPOWIEDZIALNY", 110, "w"),
        ("data_zak", "DATA ZAK.", 85, "center"),
        ("uwagi", "UWAGI", 130, "w"),
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

    odswiezTabele(tree)
    root.mainloop()


if __name__ == "__main__":
    stworzRejestrZgloszen()
