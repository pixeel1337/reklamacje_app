import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def generujSzablonMaila(nr_rek, klient, nr_projektu, opis):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f1ea;
                color: #334155;
                padding: 20px;
            }}
            .card {{
                background-color: #ffffff;
                max-width: 600px;
                margin: 0 auto;
                padding: 25px;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }}
            .header {{
                border-bottom: 2px solid #1f4e5b;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            .header h2 {{
                color: #1f4e5b;
                margin: 0;
            }}
            .info-row {{
                margin-bottom: 12px;
            }}
            .label {{
                font-weight: bold;
                font-size: 12px;
                color: #64748b;
                text-transform: uppercase;
            }}
            .value {{
                font-size: 15px;
                color: #0f172a;
                margin-top: 2px;
            }}
            .btn-container {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #f1f5f9;
                text-align: center;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                text-decoration: none;
                border-radius: 5px;
                margin: 0 8px;
            }}
            .btn-reject {{
                background-color: #ffffff;
                color: #b91c1c;
                border: 1px solid #b91c1c;
            }}
            .btn-accept {{
                background-color: #1f4e5b;
                color: #ffffff;
                border: 1px solid #1f4e5b;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h2>Oczekuje na Twoją decyzję - {nr_rek}</h2>
            </div>
            
            <p>Wpłynęło nowe zgłoszenie reklamacyjne wymagające Twojej weryfikacji.</p>
            
            <div class="info-row">
                <div class="label">Klient</div>
                <div class="value">{klient}</div>
            </div>
            
            <div class="info-row">
                <div class="label">Numer Projektu</div>
                <div class="value">{nr_projektu}</div>
            </div>
            
            <div class="info-row">
                <div class="label">Opis Zgłoszenia</div>
                <div class="value">{opis}</div>
            </div>
            
            <!-- PRZYCISKI AKCJI (Na razie makiety z pustym linkiem #) -->
            <div class="btn-container">
                <a href="#" class="btn btn-reject">✕ Odrzuć</a>
                <a href="#" class="btn btn-accept">✓ Akceptuj (Przekaż dalej)</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


def wyslijMaila(odbiorca_email, nr_rek, klient, nr_projektu, opis):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Nowa reklamacja: {nr_rek} - {klient}"
        msg["From"] = SENDER_EMAIL
        msg["To"] = odbiorca_email

        html_body = generujSzablonMaila(nr_rek, klient, nr_projektu, opis)
        msg.attach(MIMEText(html_body, "html"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, odbiorca_email, msg.as_string())

        print(f"[POWIADOMIENIE] Mail został pomylśnie wysłany do: {odbiorca_email}")
        return True

    except Exception as e:
        print(f"[BŁAD WYSYŁKI MAIL] Nie udało się wysłąc wiadomości: {e}")
        return False


if __name__ == "__main__":
    wyslijMaila(
        odbiorca_email="kamilgraczyk1@gmail.com",
        nr_rek="ZG/2026/001",
        klient="TEST_KLIENT",
        nr_projektu="12351",
        opis="Wiadomość testowa"
    )