"""Module for storage classes that work with e-mail"""
import smtplib
from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from socket import gaierror

from email_validator import validate_email
from email_validator.exceptions_types import EmailSyntaxError
from fastapi import HTTPException, status

from app.config import config


class MailSMTP(ABC):
    """
    An abstract class that implements an interface for child classes

    Methods:
        send_email: method send email to other people

    Args:
        work_email: mail from which messages are sent
        work_email_password: work email password
        smtp_server_host:

    """

    def __init__(self, work_email: str, work_email_password: str, smtp_server_host: str, smtp_server_port: int):
        self._work_email = work_email
        self._work_email_password = work_email_password
        self._smtp_server_host = smtp_server_host
        self._smtp_server_port = smtp_server_port

    @abstractmethod
    def send_email(self, to: str, message: str, subject: str):
        pass


class GmailSMTP(MailSMTP):

    def __init__(self, work_email: str, work_email_password: str, smtp_server_host: str, smtp_server_port: int):
        """Inits GmailWorker class"""
        super().__init__(work_email, work_email_password, smtp_server_host, smtp_server_port)

    def __email_config(self, msg: MIMEText, recipient: str, subject: str) -> MIMEText:
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

    def send_email(self, to: str, message: str, subject: str) -> None:
        """
        Override method sends email

        Args:
            to: recipient's email
            message: the data you want to send
            subject: email header

        """
        try:
            server = smtplib.SMTP(self._smtp_server_host, self._smtp_server_port)
            server.starttls()
            server.login(self._work_email, self._work_email_password)
            # msg = MIMEText(self._read_template(), "html")
            msg = MIMEText(message)
            msg = self.__email_config(msg=msg, recipient=to, subject=subject)
            server.sendmail(self._work_email, to, msg.as_string())
        except (gaierror, smtplib.SMTPAuthenticationError, smtplib.SMTPRecipientsRefused):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Problems sending email")


class Mail:
    """

    """

    def __init__(self, worker: MailSMTP):
        self.__worker = worker

    def send_email(self, to: str, message: str, subject: str):
        try:
            validate_email(to)
        except EmailSyntaxError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is not valid")

        self.__worker.send_email(to=to, message=message, subject=subject)


mail_worker: Mail = Mail(
    worker=GmailSMTP(work_email=config.email.work_email, work_email_password=config.email.work_email_password,
                     smtp_server_port=config.email.smtp_server_port, smtp_server_host=config.email.smtp_server_host))
