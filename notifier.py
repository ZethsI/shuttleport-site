import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email=None):
    # Gmail SMTP ayarları
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # E-posta bilgileri ortam değişkenlerinden alınır
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("EMAIL_PASSWORD")
    receiver_email = to_email or os.environ.get("EMAIL_RECEIVER")

    if not all([sender_email, sender_password, receiver_email]):
        print("❌ Gerekli ortam değişkenleri eksik. Lütfen kontrol et.")
        return

    # Mail içeriği
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ E-posta başarıyla gönderildi: {receiver_email}")
    except Exception as e:
        print(f"❌ E-posta gönderiminde hata oluştu: {e}")
