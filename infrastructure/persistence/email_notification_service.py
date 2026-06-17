import os
import smtplib
import logging
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor
from domain.interfaces.i_notification_service import INotificationService

logger = logging.getLogger(__name__)


class EmailNotificationService(INotificationService):
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "localhost")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@example.com")
        self._executor = ThreadPoolExecutor(max_workers=4)

    def _send_email(self, to: str, subject: str, body: str) -> None:
        if not self.smtp_host or self.smtp_host == "localhost":
            logger.info(f"[EMAIL] To: {to} | Subject: {subject} | Body: {body}")
            return
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = self.from_email
        msg["To"] = to
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.smtp_user:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

    def send_otp_email(self, email: str, otp: str) -> None:
        subject = "Tu código de verificación"
        body = f"<p>Tu código OTP es: <strong>{otp}</strong></p>"
        self._executor.submit(self._send_email, email, subject, body)

    def send_activation_email(self, email: str, token: str) -> None:
        subject = "Activa tu cuenta"
        activation_url = f"{{os.getenv('FRONTEND_URL', 'http://localhost:3000')}}/activate?token={token}"
        body = f"<p>Haz clic <a href='{activation_url}'>aquí</a> para activar tu cuenta.</p>"
        self._executor.submit(self._send_email, email, subject, body)
