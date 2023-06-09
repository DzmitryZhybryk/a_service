import smtplib
from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from socket import gaierror
from fastapi import HTTPException, status

from app.config import email_config


class Mail(ABC):

    def __init__(self, work_mail: str, work_mail_password: str, smtp_server_host: str, smtp_server_port: int):
        self._work_mail = work_mail
        self._work_mail_password = work_mail_password
        self._smtp_server_host = smtp_server_host
        self._smtp_server_port = smtp_server_port

    @abstractmethod
    def send_mail(self, recipient: str, send_data: str, subject: str):
        pass


class GmailWorker(Mail):

    def __init__(self, work_mail: str, work_mail_password: str, smtp_server_host: str, smtp_server_port: int):
        super().__init__(work_mail, work_mail_password, smtp_server_host, smtp_server_port)

    def __send_mail_config(self, msg: MIMEText, recipient: str, subject: str) -> MIMEText:
        msg["From"] = self._work_mail
        msg["To"] = recipient
        msg["Subject"] = subject
        msg['Reply-To'] = self._work_mail
        msg['Return-Path'] = self._work_mail
        return msg

    def send_mail(self, recipient: str, send_data: str, subject: str) -> None:
        try:
            server = smtplib.SMTP(self._smtp_server_host, self._smtp_server_port)
            server.starttls()
            server.login(self._work_mail, self._work_mail_password)
            # msg = MIMEText(self._read_template(), "html")
            msg = MIMEText(send_data)
            msg = self.__send_mail_config(msg=msg, recipient=recipient, subject=subject)
            server.sendmail(self._work_mail, recipient, msg.as_string())
        except (gaierror, smtplib.SMTPAuthenticationError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Problems sending email")


mail_worker: Mail = GmailWorker(work_mail=email_config.work_mail, work_mail_password=email_config.work_mail_password,
                                smtp_server_host=email_config.smtp_server_host,
                                smtp_server_port=email_config.smtp_server_port)

# if __name__ == '__main__':
#     test = GmailWorker(work_mail=email_config.work_mail, work_mail_password=email_config.work_mail_password,
#                        smtp_server_host=email_config.smtp_server_host, smtp_server_port=email_config.smtp_server_port)
#     test.send_mail(recipient="mr.jibrik@mail.ru", send_data="Trololo", subject="Заголовок письма")
