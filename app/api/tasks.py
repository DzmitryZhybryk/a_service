"""Module for storage Celery tasks"""
from celery import Celery

from app.utils.funcs import make_confirm_registration_url, make_confirm_registration_message
from app.utils.mail import mail_worker
from app.config import config

celery = Celery(
    'celery_api',
    broker=f'pyamqp://{config.rabbitmq.rabbitmq_default_user}:{config.rabbitmq.rabbitmq_default_pass}@rabbitmq//',
    backend=config.rabbitmq.rabbitmq_backend,
    include=['app.api.tasks']
)


@celery.task(name="app.api.make_confirm_registration_key")
def send_confirm_registration_mail(email: str, username: str, confirm_key: str) -> None:
    """
    Task for send confirm registration email

    Args:
        email: recipient email
        username: recipient username. Use for create confirm registration message
        confirm_key: confirm registration key. Use for create confirm registration URL

    """
    confirm_registration_url = make_confirm_registration_url(key=confirm_key)
    message = make_confirm_registration_message(username=username, confirm_registration_url=confirm_registration_url)
    mail_worker.send_email(to=email, message=message, subject=f"Confirm registration")


if __name__ == '__main__':
    celery.start()
