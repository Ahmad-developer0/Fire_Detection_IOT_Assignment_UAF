import smtplib
from email.mime.text import MIMEText

def send_alert(gas, temp, flame):

    sender_email = "your_email@gmail.com"
    sender_password = "Bilalsarwar123"
    receiver_email = "receiver_email@gmail.com"

    subject = "🚨 Fire and Gas Leakage Alert"

    body = f"""
    ALERT DETECTED!

    Gas Level: {gas}
    Temperature: {temp}°C
    Flame Detected: {flame}

    Immediate action required.
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("Alert sent successfully")

    except Exception as e:
        print("Error:", e)