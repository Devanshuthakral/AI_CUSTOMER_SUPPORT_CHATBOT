import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# .env file se variables load karne ke liye
load_dotenv()

def send_otp(receiver_email, otp_code):
    # 🔐 Ab credentials safe hain, .env file se aa rahe hain
    sender_email = os.getenv("SMTP_EMAIL")
    password = os.getenv("SMTP_PASSWORD")

    if not sender_email or not password:
        print("❌ Error: SMTP credentials missing in .env file!")
        return False

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "🔐 Secure OTP for Password Reset"

    body = f"""
    <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>Aapka 6-digit verification OTP hai: <b>{otp_code}</b></p>
            <p>Kripya ise kisi ke sath share na karein.</p>
        </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        
        print("✅ Email sent successfully to:", receiver_email)
        return True
    except Exception as e:
        print("❌ Mail send karne me error aaya:", e)
        return False