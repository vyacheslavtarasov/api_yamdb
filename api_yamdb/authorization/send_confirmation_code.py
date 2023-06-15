import secrets

from django.conf import settings
from django.core.mail import send_mail

random = secrets.SystemRandom()


def send_mail_code(data_code):
    """Отправка на почту сгенерированного рандомного кода."""
    email = data_code
    confirmation_code = random.randint(
        settings.MIN_CONFIRMATION_CODE,
        settings.MAX_CONFIRMATION_CODE,
    )
    send_mail(
        'Код потвержения:',
        f'Ваш код подтверждения {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=True
        # send_mail() вызовет smtplib.SMTPException, если произойдет ошибка
    )
    return str(confirmation_code)
