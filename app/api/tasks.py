"""Module for storage Celery tasks"""
from celery import Celery
from celery.utils.log import get_task_logger

from app.config import config
from email_validator import validate_email
from app.utils import decorators
from app.utils.funcs import make_confirm_registration_url, make_confirm_registration_message
from app.utils.mail import mail_worker

logger = get_task_logger(__name__)


# celery = Celery(
#     "celery_api",
#     broker=f"pyamqp://{config.rabbitmq.rabbitmq_default_user}:{config.rabbitmq.rabbitmq_default_pass}@rabbitmq//",
#     backend=config.rabbitmq.rabbitmq_backend,
#     include=["app.api.tasks"]
# )

celery = Celery(
    "celery_api",
    broker=f"pyamqp://{config.rabbitmq.rabbitmq_user_login}:{config.rabbitmq.rabbitmq_user_password}@rabbitmq//",
    backend=config.rabbitmq.rabbitmq_backend,
    include=["app.api.tasks"]
)

celery.conf.update(
    task_routes={
        "proj.tasks.send_confirm_registration_mail": {"queue": "send_confirm_registration_mail"},
    },
)


@celery.task(name="app.api.make_confirm_registration_key", ignore_result=True)
@decorators.operation_error_handler
def send_confirm_registration_email(email: str, username: str, confirm_key: str) -> None:
    """
    Task for send confirm registration email

    Args:
        email: recipient email
        username: recipient username. Use for create confirm registration message
        confirm_key: confirm registration key. Use for create confirm registration URL

    Raises:
        HTTP_500_INTERNAL_SERVER_ERROR if message broker not available

    """
    validate_email(email)
    confirm_registration_url = make_confirm_registration_url(key=confirm_key)
    message = make_confirm_registration_message(username=username, confirm_registration_url=confirm_registration_url)
    mail_worker.send_email(to=email, message=message, subject=f"Confirm registration")


if __name__ == '__main__':
    celery.start()
