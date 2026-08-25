import threading
import tkinter as tk
from tkinter import messagebox, ttk

from baza import aktualizujReklamacje, pobierzReklamacjePoNumerze
from obsluga_maili import MAPA_EMAILI, wyslijMaila
from config import DYREKTORZY, PRACOWNICY


def otworzPanelDyrektora(
    parent_window, nr_rek_start="ZG/2026/001", odswiez_callback=None
):
    dir_window = tk.Toplevel(parent_window)
    dir_window.title("Decyzja Dyrektora")
    dir_window.geometry("750x850")
    dir_window.configure(bg="#f4f1ea")

    dir_window.transient(parent_window)
    dir_window.grab_set()

    aktualna_reklamacja = {}

    top_bar = tk.Frame(dir_window, bg="#f4f1ea", padx=20, pady=15)
    top_bar.pack(fill="x")

    btn_back = tk.Button(
        top_bar,
        text="← Wróć do rejestru",
        font=("Segoe UI", 10, "bold"),
        bg="#f4f1ea",
        fg="#1f4e5b",
        bd=0,
        cursor="hand2",
        command=dir_window.destroy,
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
        search_box,
        font=("Segoe UI", 9, "bold"),
        width=14,
        bd=1,
        relief="solid",
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

    content_frame = tk.Frame(dir_window, bg="#f4f1ea", padx=20)
    content_frame.pack(fill="both", expand=True)

    sec_roles = tk.Frame(content_frame, bg="#f8f6f0", bd=1, relief="solid")
    sec_roles.pack(fill="x", pady=(0, 15))

    roles_body = tk.Frame(sec_roles, bg="#f8f6f0", padx=15, pady=12)
    roles_body.pack(fill="x")
    roles_body.columnconfigure(0, weight=1)
    roles_body.columnconfigure(1, weight=1)

    f_role1 = tk.Frame(roles_body, bg="#f8f6f0")
    f_role1.grid(row=0, column=0, sticky="ew", padx=(0, 10))
    tk.Label(
        f_role1,
        text="PRACUJESZ JAKO",
        font=("Segoe UI", 8, "bold"),
        bg="#f8f6f0",
        fg="#64748b",
    ).pack(anchor="w")
    combo_role1 = ttk.Combobox(
        f_role1,
        values=["Dyrektor obszaru", "Osoba rejestrująca", "Serwisant"],
        state="readonly",
        font=("Segoe UI", 10),
    )
    combo_role1.set("Dyrektor obszaru")
    combo_role1.pack(fill="x", pady=(4, 0), ipady=3)

    f_role2 = tk.Frame(roles_body, bg="#f8f6f0")
    f_role2.grid(row=0, column=1, sticky="ew")
    tk.Label(
        f_role2,
        text="ZALOGOWANY JAKO (DYREKTOR)",
        font=("Segoe UI", 8, "bold"),
        bg="#f8f6f0",
        fg="#64748b",
    ).pack(anchor="w")
    combo_role2 = ttk.Combobox(
        f_role2,
        values=DYREKTORZY,
        state="readonly",
        font=("Segoe UI", 10),
    )
    combo_role2.set(DYREKTORZY[0])
    combo_role2.pack(fill="x", pady=(4, 0), ipady=3)

    sec1_card = tk.Frame(content_frame, bg="#f8fafc", bd=1, relief="solid")
    sec1_card.pack(fill="x", pady=(0, 15))

    card1_body = tk.Frame(sec1_card, bg="#f8fafc", padx=15, pady=20)
    card1_body.pack(fill="x")

    sec1_hdr = tk.Frame(card1_body, bg="#f8fafc")
    sec1_hdr.pack(fill="x", pady=(0, 10))

    tk.Label(
        sec1_hdr,
        text="❶  1 · REJESTRACJA ZGŁOSZENIA",
        font=("Segoe UI", 10, "bold"),
        bg="#f8fafc",
        fg="#64748b",
    ).pack(side="left")
    tk.Label(
        sec1_hdr,
        text="wysłano do dyrektora",
        font=("Segoe UI", 8, "italic"),
        bg="#f8fafc",
        fg="#94a3b8",
    ).pack(side="right")

    row1 = tk.Frame(card1_body, bg="#f8fafc")
    row1.pack(fill="x")
    row1.columnconfigure(0, weight=1)
    row1.columnconfigure(1, weight=1)

    f_klient = tk.Frame(row1, bg="#f8fafc")
    f_klient.grid(row=0, column=0, sticky="ew", padx=(0, 10))
    tk.Label(
        f_klient,
        text="KLIENT",
        font=("Segoe UI", 8, "bold"),
        bg="#f8fafc",
        fg="#94a3b8",
    ).pack(anchor="w")
    e_klient = tk.Entry(
        f_klient,
        font=("Segoe UI", 10),
        bd=1,
        relief="solid",
        fg="#64748b",
        bg="#f1f5f9",
    )
    e_klient.pack(fill="x", ipady=4, pady=(2, 0))

    f_projekt = tk.Frame(row1, bg="#f8fafc")
    f_projekt.grid(row=0, column=1, sticky="ew")
    tk.Label(
        f_projekt,
        text="NR PROJEKTU",
        font=("Segoe UI", 8, "bold"),
        bg="#f8fafc",
        fg="#94a3b8",
    ).pack(anchor="w")
    e_projekt = tk.Entry(
        f_projekt,
        font=("Segoe UI", 10),
        bd=1,
        relief="solid",
        fg="#64748b",
        bg="#f1f5f9",
    )
    e_projekt.pack(fill="x", ipady=4, pady=(2, 0))

    sec2_card = tk.Frame(content_frame, bg="#ffffff", bd=1, relief="solid")
    sec2_card.pack(fill="both", expand=True, pady=(0, 20))

    card2_body = tk.Frame(sec2_card, bg="#ffffff", padx=20, pady=15)
    card2_body.pack(fill="both", expand=True)

    tk.Label(
        card2_body,
        text="➤  2 · DECYZJA DYREKTORA",
        font=("Segoe UI", 11, "bold"),
        bg="#ffffff",
        fg="#0f172a",
    ).pack(anchor="w", pady=(0, 10))

    lbl_dyrektor_name = tk.Label(
        card2_body,
        text=f"Dyrektor obszaru: {combo_role2.get()}",
        font=("Segoe UI", 9, "bold"),
        bg="#ffffff",
        fg="#334155",
    )
    lbl_dyrektor_name.pack(anchor="w", pady=(0, 12))

    def zaktualizuj_dyrektora(e=None):
        lbl_dyrektor_name.config(text=f"Dyrektor obszaru: {combo_role2.get()}")

    combo_role2.bind("<<ComboboxSelected>>", zaktualizuj_dyrektora)

    dec_btns_frame = tk.Frame(card2_body, bg="#ffffff")
    dec_btns_frame.pack(anchor="w", pady=(0, 15))

    btn_reject = tk.Button(
        dec_btns_frame,
        text="✕  Odrzuć",
        font=("Segoe UI", 9, "bold"),
        bg="#ffffff",
        fg="#b91c1c",
        activebackground="#fef2f2",
        activeforeground="#b91c1c",
        bd=1,
        relief="solid",
        highlightthickness=0,
        padx=16,
        pady=6,
        cursor="hand2",
    )
    btn_reject.pack(side="left", padx=(0, 10))

    btn_next = tk.Button(
        dec_btns_frame,
        text="➤  Prześlij dalej",
        font=("Segoe UI", 9, "bold"),
        bg="#1f4e5b",
        fg="white",
        activebackground="#2d6a78",
        activeforeground="white",
        bd=0,
        padx=16,
        pady=7,
        cursor="hand2",
    )
    btn_next.pack(side="left")

    sub_card_pass = tk.Frame(card2_body, bg="#f8f6f0", bd=1, relief="solid")
    sub_body_pass = tk.Frame(sub_card_pass, bg="#f8f6f0", padx=15, pady=15)
    sub_body_pass.pack(fill="x")

    tk.Label(
        sub_body_pass,
        text="WYBIERZ OSOBĘ ODPOWIEDZIALNĄ (Z ZESPOŁU) *",
        font=("Segoe UI", 8, "bold"),
        bg="#f8f6f0",
        fg="#b91c1c",
    ).pack(anchor="w")

    combo_resp = ttk.Combobox(
        sub_body_pass,
        values=PRACOWNICY,
        state="readonly",
        font=("Segoe UI", 10),
    )
    combo_resp.set(PRACOWNICY[0])
    combo_resp.pack(fill="x", ipady=3, pady=(5, 15))

    btn_confirm = tk.Button(
        sub_body_pass,
        text="Potwierdź przekazanie i wyślij e-mail",
        font=("Segoe UI", 9, "bold"),
        bg="#1f4e5b",
        fg="white",
        activebackground="#2d6a78",
        activeforeground="white",
        bd=0,
        padx=16,
        pady=7,
        cursor="hand2",
    )
    btn_confirm.pack(anchor="w")

    sub_card_reject = tk.Frame(card2_body, bg="#fef2f2", bd=1, relief="solid")
    sub_body_reject = tk.Frame(sub_card_reject, bg="#fef2f2", padx=15, pady=15)
    sub_body_reject.pack(fill="x")

    tk.Label(
        sub_body_reject,
        text="PODAJ POWÓD ODRZUCENIA *",
        font=("Segoe UI", 8, "bold"),
        bg="#fef2f2",
        fg="#b91c1c",
    ).pack(anchor="w")

    txt_powod = tk.Text(
        sub_body_reject, font=("Segoe UI", 9), height=3, bd=1, relief="solid"
    )
    txt_powod.pack(fill="x", pady=(5, 15))

    btn_confirm_reject = tk.Button(
        sub_body_reject,
        text="Potwierdź odrzucenie zgłoszenia",
        font=("Segoe UI", 9, "bold"),
        bg="#b91c1c",
        fg="white",
        activebackground="#dc2626",
        activeforeground="white",
        bd=0,
        padx=16,
        pady=7,
        cursor="hand2",
    )
    btn_confirm_reject.pack(anchor="w")

    def pokaz_karty(tryb):
        if tryb == "pass":
            sub_card_reject.pack_forget()
            sub_card_pass.pack(fill="x", pady=(5, 0))
            btn_next.config(bg="#1f4e5b", fg="white")
            btn_reject.config(bg="#ffffff", fg="#b91c1c")
        elif tryb == "reject":
            sub_card_pass.pack_forget()
            sub_card_reject.pack(fill="x", pady=(5, 0))
            btn_reject.config(bg="#b91c1c", fg="white")
            btn_next.config(bg="#ffffff", fg="#475569")

    btn_next.config(command=lambda: pokaz_karty("pass"))
    btn_reject.config(command=lambda: pokaz_karty("reject"))

    def wczytaj_dane():
        nonlocal aktualna_reklamacja
        nr_szukany = e_szukaj_nr.get().strip().upper().replace("_", "/")

        znaleziona = pobierzReklamacjePoNumerze(nr_szukany)
        if not znaleziona:
            messagebox.showwarning(
                "Nie znaleziono",
                f"Nie odnaleziono w bazie zgłoszenia o numerze: {nr_szukany}",
            )
            aktualna_reklamacja = {}
            return

        aktualna_reklamacja = znaleziona
        status = znaleziona.get("status", "NOWE")
        lbl_status_badge.config(text=f" {status} ")

        e_klient.configure(state="normal")
        e_klient.delete(0, "end")
        e_klient.insert(0, znaleziona.get("klient", ""))
        e_klient.configure(state="disabled")

        e_projekt.configure(state="normal")
        e_projekt.delete(0, "end")
        e_projekt.insert(
            0,
            znaleziona.get("nr_projektu")
            or znaleziona.get("nr_zadania", ""),
        )
        e_projekt.configure(state="disabled")

        if znaleziona.get("odpowiedzialny") in PRACOWNICY:
            combo_resp.set(znaleziona.get("odpowiedzialny"))

        txt_powod.delete("1.0", "end")
        txt_powod.insert("1.0", znaleziona.get("powod_odrzucenia", ""))

    btn_laduj.config(command=wczytaj_dane)

    def potwierdz_przekazanie():
        if not aktualna_reklamacja:
            messagebox.showwarning(
                "Brak danych",
                "Najpierw wczytaj zgłoszenie przyciskiem '🔍 Wczytaj'!",
            )
            return

        nr_szukany = e_szukaj_nr.get().strip().upper().replace("_", "/")
        wybrany_pracownik = combo_resp.get()
        dyrektor = combo_role2.get()

        dane_aktualizacji = {
            "status": "W TRAKCIE",
            "odpowiedzialny": wybrany_pracownik,
            "dyrektor": dyrektor,
        }

        wynik = aktualizujReklamacje(
            nr_szukany, dane_aktualizacji, regeneruj_pliki=True
        )
        if not wynik:
            messagebox.showerror(
                "Błąd", f"Nie udało się zaktualizować zgłoszenia {nr_szukany}."
            )
            return

        klient_nazwa = wynik.get("klient", "")
        nr_proj = wynik.get("nr_projektu") or wynik.get("nr_zadania", "")
        opis_val = wynik.get("opis", "")

        threading.Thread(
            target=wyslijMaila,
            kwargs={
                "odbiorca": wybrany_pracownik,
                "nr_rek": nr_szukany,
                "klient": klient_nazwa,
                "nr_projektu": nr_proj,
                "opis": opis_val,
                "typ": "pracownik",
            },
            daemon=True,
        ).start()

        messagebox.showinfo(
            "Sukces",
            f"Zgłoszenie {nr_szukany} zostało przekazane do: {wybrany_pracownik}.\nStatus zmieniony na W TRAKCIE, a powiadomienie e-mail zostało wysłane.",
        )
        if odswiez_callback:
            odswiez_callback()
        dir_window.destroy()

    def potwierdz_odrzucenie():
        if not aktualna_reklamacja:
            messagebox.showwarning(
                "Brak danych",
                "Najpierw wczytaj zgłoszenie przyciskiem '🔍 Wczytaj'!",
            )
            return

        powod_val = txt_powod.get("1.0", "end-1c").strip()
        if not powod_val:
            messagebox.showwarning(
                "Brak powodu", "Podaj powód odrzucenia reklamacji!"
            )
            return

        nr_szukany = e_szukaj_nr.get().strip().upper().replace("_", "/")
        dyrektor = combo_role2.get()

        dane_aktualizacji = {
            "status": "ODRZUCONE",
            "powod_odrzucenia": powod_val,
            "dyrektor": dyrektor,
        }

        wynik = aktualizujReklamacje(
            nr_szukany, dane_aktualizacji, regeneruj_pliki=True
        )
        if not wynik:
            messagebox.showerror(
                "Błąd", f"Nie udało się odrzucić zgłoszenia {nr_szukany}."
            )
            return

        messagebox.showinfo(
            "Odrzucono", f"Zgłoszenie {nr_szukany} zostało odrzucone."
        )
        if odswiez_callback:
            odswiez_callback()
        dir_window.destroy()

    btn_confirm.config(command=potwierdz_przekazanie)
    btn_confirm_reject.config(command=potwierdz_odrzucenie)

    pokaz_karty("pass")
    wczytaj_dane()

    return dir_window


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    panel = otworzPanelDyrektora(root, "ZG/2026/001")
    panel.transient("")  # Odpięcie od ukrytego roota
    panel.protocol("WM_DELETE_WINDOW", root.destroy)
    
    root.mainloop()