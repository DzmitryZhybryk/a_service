import smtplib
from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from socket import gaierror
from fastapi import HTTPException, status

from app.config import email_config


class EMail(ABC):
    """
    Abstract class, implements contracts for child classes

    Args:
        work_email: email from which messages are sent
        work_email_password: password for work email
        smtp_server_host: outgoing email server host
        smtp_server_port: outgoing email server port

    """

    def __init__(self, work_email: str, work_email_password: str, smtp_server_host: str, smtp_server_port: int):
        """Inits EMail class"""
        self._work_email = work_email
        self._work_email_password = work_email_password
        self._smtp_server_host = smtp_server_host
        self._smtp_server_port = smtp_server_port

    @abstractmethod
    def send_email(self, recipient: str, send_data: str, subject: str):
        pass


class GmailWorker(EMail):

    def __init__(self, work_email: str, work_email_password: str, smtp_server_host: str, smtp_server_port: int):
        """Inits GmailWorker class"""
        super().__init__(work_email, work_email_password, smtp_server_host, smtp_server_port)

    def __send_email_config(self, msg: MIMEText, recipient: str, subject: str) -> MIMEText:
        """
        Method makes send email config

        Args:
            msg: MIMEText object with metadata for sending email
            recipient: recipient's email
            subject: email header

        Returns:
            MIMEText object ready to send

        """
        msg["From"] = self._work_email
        msg["To"] = recipient
        msg["Subject"] = subject
        msg['Reply-To'] = self._work_email
        msg['Return-Path'] = self._work_email
        return msg

    def send_email(self, recipient: str, send_data: str, subject: str) -> None:
        """
        Method sends email

        Args:
            recipient: recipient's email
            send_data: the data you want to send
            subject: email header

        """
        try:
            server = smtplib.SMTP(self._smtp_server_host, self._smtp_server_port)
            server.starttls()
            server.login(self._work_email, self._work_email_password)
            # msg = MIMEText(self._read_template(), "html")
            msg = MIMEText(send_data)
            msg = self.__send_email_config(msg=msg, recipient=recipient, subject=subject)
            server.sendmail(self._work_email, recipient, msg.as_string())
        except (gaierror, smtplib.SMTPAuthenticationError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Problems sending email")


mail_worker: EMail = GmailWorker(work_email=email_config.work_email,
                                 work_email_password=email_config.work_email_password,
                                 smtp_server_host=email_config.smtp_server_host,
                                 smtp_server_port=email_config.smtp_server_port)
