import tkinter as tk
from tkinter import ttk 

def otworzPanelDyrektora(parent_window):
    dir_window = tk.Toplevel(parent_window)
    dir_window.title("Decyzja Dyrektora")
    dir_window.geometry("750x850")
    dir_window.configure(bg="#f4f1ea")

    dir_window.transient(parent_window)
    dir_window.grab_set()


    # Pasek górny
    top_bar = tk.Frame(dir_window, bg="#f4f1ea", padx=20, pady=15)
    top_bar.pack(fill="x")

    btn_back = tk.Button(top_bar, text="← Wróć do rejestru", font=("Segoe UI", 10, "bold"),
                         bg="#f4f1ea", fg="#1f4e5b", bd=0, cursor="hand2")
    btn_back.pack(side="left")

    badge_frame = tk.Frame(top_bar, bg="#f4f1ea")
    badge_frame.pack(side="right")

    tk.Label(badge_frame, text="ZG/2026/001", font=("Segoe UI", 10, "bold"), bg="#f4f1ea", fg="#334155").pack(side="left", padx=(0, 5))
    tk.Label(badge_frame, text=" W TRAKCIE ", font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#d97706", relief="solid", bd=1).pack(side="left")


    content_frame = tk.Frame(dir_window, bg="#f4f1ea", padx=20)
    content_frame.pack(fill="both", expand=True)

    # Sekcja: Role 

    sec_roles = tk.Frame(content_frame, bg="#f8f6f0", bd=1, relief="solid")
    sec_roles.pack(fill="x", pady=(0, 15))

    roles_body = tk.Frame(sec_roles, bg="#f8f6f0", padx=15, pady=12)
    roles_body.pack(fill="x")
    roles_body.columnconfigure(0, weight=1)
    roles_body.columnconfigure(1, weight=1)

    
    # Sekcja: Role -> Pracujesz jako
    f_role1 = tk.Frame(roles_body, bg="#f8f6f0")
    f_role1.grid(row=0, column=0, sticky="ew", padx=(0, 10))
    tk.Label(f_role1, text="PRACUJESZ JAKO", font=("Segoe UI", 8, "bold"), bg="#f8f6f0", fg="#64748b").pack(anchor="w")
    combo_role1 = ttk.Combobox(f_role1, values=["Dyrektor obszaru", "Osoba rejestrująca", "Serwisant"], state="readonly", font=("Segoe UI", 10))
    combo_role1.set("Dyrektor obszaru")
    combo_role1.pack(fill="x", pady=(4, 0), ipady=3)


    # Sekcja: Role -> Zalogowany jako (Osoba)
    f_role2 = tk.Frame(roles_body, bg="#f8f6f0")
    f_role2.grid(row=0, column=1, sticky="ew")
    tk.Label(f_role2, text="ZALOGOWANY JAKO (DYREKTOR)", font=("Segoe UI", 8, "bold"), bg="#f8f6f0", fg="#64748b").pack(anchor="w")
    combo_role2 = ttk.Combobox(f_role2, values=["Anna Kowalska", "Marek Nowak", "Piotr Wiśniewski"], state="readonly", font=("Segoe UI", 10))
    combo_role2.set("Anna Kowalska")
    combo_role2.pack(fill="x", pady=(4, 0), ipady=3)


    # Sekcja: Rejestracja Zgłoszenia
    sec1_card = tk.Frame(content_frame, bg="#f8fafc", bd=1, relief="solid")
    sec1_card.pack(fill="x", pady=(0, 15))

    card1_body = tk.Frame(sec1_card, bg="#f8fafc", padx=15, pady=20)
    card1_body.pack(fill="x")

    # Naglówek sekcji   
    sec1_hdr = tk.Frame(card1_body, bg="#f8fafc")
    sec1_hdr.pack(fill="x", pady=(0, 10))

    tk.Label(sec1_hdr, text="❶  1 · REJESTRACJA ZGŁOSZENIA", font=("Segoe UI", 10, "bold"), bg="#f8fafc", fg="#64748b").pack(side="left")
    tk.Label(sec1_hdr, text="wysłano do dyrektora", font=("Segoe UI", 8, "italic"), bg="#f8fafc", fg="#94a3b8").pack(side="right")

    # Wiersz: Klient + Nr Projektu

    row1 = tk.Frame(card1_body, bg="#f8fafc")
    row1.pack(fill="x")
    row1.columnconfigure(0, weight=1)
    row1.columnconfigure(1, weight=1)

    f_klient = tk.Frame(row1, bg="#f8fafc")
    f_klient.grid(row=0, column=0, sticky="ew", padx=(0, 10))
    tk.Label(f_klient, text="KLIENT", font=("Segoe UI", 8, "bold"), bg="#f8fafc", fg="#94a3b8").pack(anchor="w")
    e_klient = tk.Entry(f_klient, font=("Segoe UI", 10), bd=1, relief="solid", fg="#64748b", bg="#f1f5f9")
    e_klient.insert(0, "ORLEN")
    e_klient.configure(state="disabled")
    e_klient.pack(fill="x", ipady=4, pady=(2, 0))

    f_projekt = tk.Frame(row1, bg="#f8fafc")
    f_projekt.grid(row=0, column=1, sticky="ew")
    tk.Label(f_projekt, text="NR PROJEKTU", font=("Segoe UI", 8, "bold"), bg="#f8fafc", fg="#94a3b8").pack(anchor="w")
    e_projekt = tk.Entry(f_projekt, font=("Segoe UI", 10), bd=1, relief="solid", fg="#64748b", bg="#f1f5f9")
    e_projekt.insert(0, "2334444")
    e_projekt.configure(state="disabled")
    e_projekt.pack(fill="x", ipady=4, pady=(2, 0))


    # Sekcja: Decyzja Dyrektora
    sec2_card = tk.Frame(content_frame, bg="#ffffff", bd=1, relief="solid")
    sec2_card.pack(fill="both", expand=True, pady=(0, 20))

    card2_body = tk.Frame(sec2_card, bg="#ffffff", padx=20, pady=15)
    card2_body.pack(fill="both", expand=True)

    tk.Label(card2_body, text="➤  2 · DECYZJA DYREKTORA", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#0f172a").pack(anchor="w", pady=(0, 10))
    tk.Label(card2_body, text="Dyrektor obszaru: Anna Kowalska", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#334155").pack(anchor="w", pady=(0, 12))
    
    # Przyciski akcji
    dec_btns_frame = tk.Frame(card2_body, bg="#ffffff")
    dec_btns_frame.pack(anchor="w", pady=(0, 15))

    btn_reject = tk.Button(dec_btns_frame, text="✕  Odrzuć", font=("Segoe UI", 9, "bold"),
                           bg="#ffffff", fg="#b91c1c", activebackground="#fef2f2", activeforeground="#b91c1c",
                           bd=1, relief="solid", highlightthickness=0, padx=16, pady=6, cursor="hand2")
    btn_reject.pack(side="left", padx=(0, 10))

    btn_next = tk.Button(dec_btns_frame, text="➤  Prześlij dalej", font=("Segoe UI", 9, "bold"),
                         bg="#1f4e5b", fg="white", activebackground="#2d6a78", activeforeground="white",
                         bd=0, padx=16, pady=7, cursor="hand2")
    btn_next.pack(side="left")

    # Karta przesłania do osoby odpowiedzialnej
    sub_card = tk.Frame(card2_body, bg="#f8f6f0", bd=1, relief="solid")
    sub_card.pack(fill="x", pady=(5, 0))

    sub_body = tk.Frame(sub_card, bg="#f8f6f0", padx=15, pady=15)
    sub_body.pack(fill="x")

    tk.Label(sub_body, text="WYBIERZ OSOBĘ ODPOWIEDZIALNĄ (Z ZESPOŁU) *", font=("Segoe UI", 8, "bold"), bg="#f8f6f0", fg="#b91c1c").pack(anchor="w")
    
    combo_resp = ttk.Combobox(sub_body, values=["Marek Zieliński", "Piotr Kowalski", "Anna Nowak"], font=("Segoe UI", 10))
    combo_resp.set("Marek Zieliński")
    combo_resp.pack(fill="x", ipady=3, pady=(5, 15))

    btn_confirm = tk.Button(sub_body, text="Potwierdź przekazanie", font=("Segoe UI", 9, "bold"),
                            bg="#1f4e5b", fg="white", activebackground="#2d6a78", activeforeground="white",
                            bd=0, padx=16, pady=7, cursor="hand2")
    btn_confirm.pack(anchor="w")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Testowanie widoku")
    root.geometry("300x100")

    label = tk.Label(root, text="Okno główne w tle (nie zamykaj)")
    label.pack(expand=True)

    otworzPanelDyrektora(root)

    root.mainloop()