import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

LOG_PATH = os.path.join(os.path.dirname(__file__), "run_history.log")

def read_recent_logs(hours=12):
    if not os.path.exists(LOG_PATH):
        return "No log file found."

    cutoff = datetime.now() - timedelta(hours=hours)
    lines = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f.readlines():
            try:
                timestamp = line.split("]")[0].strip("[")
                t = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
                if t > cutoff:
                    lines.append(line.strip())
            except Exception:
                continue
    return "\n".join(lines) if lines else "No recent updates found."

def send_digest_email():
    sender = os.getenv("MAIL_SENDER")
    password = os.getenv("MAIL_PASSWORD")
    recipient = os.getenv("MAIL_RECEIVER")

    if not all([sender, password, recipient]):
        raise ValueError("Missing one or more email environment variables.")

    logs = read_recent_logs()
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = f"Job Tracker Digest — {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    body = f"""<h3>Job Tracker Update Summary (Last 12 Hours)</h3>
<pre>{logs}</pre>
<p>— Automated by GitHub Actions</p>"""
    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

    print("✅ Digest email sent successfully.")

if __name__ == "__main__":
    send_digest_email()