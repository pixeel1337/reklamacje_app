import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Słownik przypisujący pracownika do jego adresu e-mail
MAPA_EMAILI = {
    "Marek Zieliński": "kamilgraczyk1@gmail.com",
    "Piotr Kowalski": "kamilgraczyk1@gmail.com",
    "Marta Wiśniewska": "kamilgraczyk1@gmail.com",
    "Jan Kowalski": "kamilgraczyk1@gmail.com",
    "Anna Nowak": "kamilgraczyk1@gmail.com",
    "Anna Kowalska": "kamilgraczyk1@gmail.com",
    "Marek Nowak": "kamilgraczyk1@gmail.com",
    "Piotr Wiśniewski": "kamilgraczyk1@gmail.com",
}


def generujSzablonDyrektora(nr_rek, klient, nr_projektu, opis):
    """Generuje szablon HTML dla Dyrektora w celu podjęcia decyzji."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #f4f1ea; color: #334155; padding: 20px; }}
            .card {{ background-color: #ffffff; max-width: 600px; margin: 0 auto; padding: 25px; border-radius: 8px; border: 1px solid #e2e8f0; }}
            .header {{ border-bottom: 2px solid #1f4e5b; padding-bottom: 10px; margin-bottom: 20px; }}
            .header h2 {{ color: #1f4e5b; margin: 0; }}
            .info-row {{ margin-bottom: 12px; }}
            .label {{ font-weight: bold; font-size: 12px; color: #64748b; text-transform: uppercase; }}
            .value {{ font-size: 15px; color: #0f172a; margin-top: 2px; }}
            .btn-container {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #f1f5f9; text-align: center; }}
            .btn {{ display: inline-block; padding: 12px 24px; font-size: 14px; font-weight: bold; text-decoration: none; border-radius: 5px; margin: 0 8px; }}
            .btn-reject {{ background-color: #ffffff; color: #b91c1c; border: 1px solid #b91c1c; }}
            .btn-accept {{ background-color: #1f4e5b; color: #ffffff; border: 1px solid #1f4e5b; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h2>Oczekuje na Twoją decyzję - {nr_rek}</h2>
            </div>
            <p>Wpłynęło nowe zgłoszenie reklamacyjne wymagające Twojej weryfikacji.</p>
            <div class="info-row"><div class="label">Klient</div><div class="value">{klient or '—'}</div></div>
            <div class="info-row"><div class="label">Numer Projektu</div><div class="value">{nr_projektu or '—'}</div></div>
            <div class="info-row"><div class="label">Opis Zgłoszenia</div><div class="value">{opis or '—'}</div></div>
            <div class="btn-container">
                <a href="#" class="btn btn-reject">✕ Odrzuć</a>
                <a href="#" class="btn btn-accept">✓ Akceptuj (Przekaż dalej)</a>
            </div>
        </div>
    </body>
    </html>
    """


def generujSzablonPracownika(pracownik_nazwa, nr_rek, klient, nr_projektu, opis):
    """Generuje szablon HTML dla Pracownika przydzielonego do realizacji."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #f4f1ea; color: #334155; padding: 20px; }}
            .card {{ background-color: #ffffff; max-width: 600px; margin: 0 auto; padding: 25px; border-radius: 8px; border: 1px solid #e2e8f0; }}
            .header {{ border-bottom: 2px solid #1f4e5b; padding-bottom: 10px; margin-bottom: 20px; }}
            .header h2 {{ color: #1f4e5b; margin: 0; }}
            .info-row {{ margin-bottom: 12px; }}
            .label {{ font-weight: bold; font-size: 12px; color: #64748b; text-transform: uppercase; }}
            .value {{ font-size: 15px; color: #0f172a; margin-top: 2px; }}
            .btn-container {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #f1f5f9; text-align: center; }}
            .btn-open {{ background-color: #1f4e5b; color: #ffffff; padding: 12px 28px; font-size: 14px; font-weight: bold; text-decoration: none; border-radius: 5px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h2>Cześć {pracownik_nazwa}! Przydzielono reklamację: {nr_rek}</h2>
            </div>
            <p>Dyrektor przekazał do Twojej realizacji poniższe zgłoszenie reklamacyjne.</p>
            
            <div class="info-row"><div class="label">Klient</div><div class="value">{klient or '—'}</div></div>
            <div class="info-row"><div class="label">Numer Projektu</div><div class="value">{nr_projektu or '—'}</div></div>
            <div class="info-row"><div class="label">Opis Zgłoszenia</div><div class="value">{opis or '—'}</div></div>
            
            <div class="btn-container">
                <a href="#" class="btn-open">➔ Przejdź do zgłoszenia w aplikacji</a>
            </div>
        </div>
    </body>
    </html>
    """


def wyslijMaila(odbiorca, nr_rek, klient="", nr_projektu="", opis="", typ="pracownik", nr_zadania=None):
    """
    Wysyła sformatowaną wiadomość e-mail do wskazanego odbiorcy.
    Automatycznie mapuje nazwiska na adresy e-mail ze słownika MAPA_EMAILI.
    """
    if nr_zadania and not nr_projektu:
        nr_projektu = nr_zadania

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("[BŁĄD WYSYŁKI MAIL]: Brak skonfigurowanych danych SENDER_EMAIL / SENDER_PASSWORD w pliku .env!")
        return False

    odbiorca_email = MAPA_EMAILI.get(odbiorca, odbiorca)

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = f"System Reklamacji <{SENDER_EMAIL}>"
        msg["To"] = odbiorca_email

        if typ == "pracownik":
            msg["Subject"] = f"🔔 Przydzielono reklamację: {nr_rek} - {klient}"
            html_body = generujSzablonPracownika(odbiorca, nr_rek, klient, nr_projektu, opis)
        else:
            msg["Subject"] = f"Nowa reklamacja: {nr_rek} - {klient}"
            html_body = generujSzablonDyrektora(nr_rek, klient, nr_projektu, opis)

        msg.attach(MIMEText(html_body, "html", "utf-8"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, odbiorca_email, msg.as_string())
        server.quit()

        print(f"[POWIADOMIENIE] Mail został pomyślnie wysłany do: {odbiorca} ({odbiorca_email})")
        return True

    except Exception as e:
        print(f"[BŁĄD WYSYŁKI MAIL] Nie udało się wysłać wiadomości: {e}")
        return False

