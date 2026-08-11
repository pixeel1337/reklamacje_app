import tkinter as tk
from tkinter import ttk


from formularz import otworzFormularzDodawania
from formularz_pracownika import otworzPanelRealizacji
from formularz_dyrektora import otworzPanelDyrektora

def otworzZintegrowanyPanel(parent_window):
    win = tk.Toplevel(parent_window)
    win.title("Obsługa zgłoszenia")
    win.geometry("780x900")
    win.geometry("780x900")
    win.configure(bg="#f4f1ea")

    win.transient(parent_window)
    win.grab_set()

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

    badge_frame = tk.Frame(top_bar, bg="#f4f1ea")
    badge_frame.pack(side="right")
    tk.Label(
        badge_frame,
        text="ZG/2026/023",
        font=("Segoe UI", 10, "bold"),
        bg="#f4f1ea",
        fg="#334155",
    ).pack(side="left", padx=(0, 5))

    lbl_status = tk.Label(
        badge_frame,
        text=" NOWE ",
        font=("Segoe UI", 8, "bold"),
        bg="#ffffff",
        fg="#1f4e5b",
        relief="solid",
        bd=1,
    )
    lbl_status.pack(side="left")

    role_frame = tk.Frame(win, bg="#f4f1ea", padx=20)
    role_frame.pack(fill="x", pady=(0, 10))

    role_card = tk.Frame(role_frame, bg="#f8f6f0", bd=1, relief="solid")
    role_card.pack(fill="x")

    role_body = tk.Frame(role_card, bg="#f8f6f0", padx=15, pady=10)
    role_body.pack(fill="x")

    tk.Label(
        role_body,
        text="Pracujesz jako",
        font=("Segoe UI", 8, "bold"),
        bg="#f8f6f0",
        fg="#64748b",
    ).pack(anchor="w")

    combo_rola = ttk.Combobox(
        role_body,
        values=["Osoba rejestrująca", "Dyrektor obszaru", "Serwisant"],
        state="readonly",
        font=("Segoe UI", 10),
    )
    combo_rola.set("Osoba rejestrująca")
    combo_rola.pack(fill="x", pady=(3, 0), ipady=3)

    canvas = tk.Canvas(win, bg="#f4f1ea", highlightthickness=0)
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f4f1ea", padx=20)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=720)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, pady=(0, 20))
    scrollbar.pack(side="right", fill="y", pady=(0, 20))

    view_rejestracja = otworzFormularzDodawania(scroll_frame)
    view_dyrektor = otworzPanelDyrektora(scroll_frame)
    view_realizacja = otworzPanelRealizacji(scroll_frame)

    def przelaczWidok(event=None):
        wybrana_rola = combo_rola.get()

        view_rejestracja.pack_forget()
        view_dyrektor.pack_forget()
        view_realizacja.pack_forget()

        if wybrana_rola == "Osoba rejestrująca":
            view_rejestracja.pack(fill="x", pady=5)
            lbl_status.config(text=" NOWE ", fg="#1f4e5b")

        elif wybrana_rola == "Dyrektor obszaru":
            view_dyrektor.pack(fill="x", pady=5)
            lbl_status.config(text=" OCZEKUJE NA DECYZJĘ ", fg="#d97706")

        elif wybrana_rola == "Serwisant":
            view_realizacja.pack(fill="x", pady=5)
            lbl_status.config(text=" W TRAKCIE ", fg="#a51d24")


    combo_rola.bind("<<ComboboxSelected>>", przelaczWidok)

    przelaczWidok()