from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

from config.settings import USER_MIN_AGE, RESTRICTED_EMAIL_DOMAIN


def check_birth_date(value: date) -> None:
    """
    Валидатор, который проверяет что возраст пользователя не меньше, чем заданный сервисом

    :param value: Значение даты, переданное пользователем.
    :return: None
    """
    difference = relativedelta(date.today(), value).years

    if difference < USER_MIN_AGE:
        raise ValidationError(
            f"Your age is {value}. You must be an 9 years or older for register"
        )


def check_email_domain(value: str) -> None:
    """
    Валидатор, который проверяет доменное имя email пользователя на соответствие требованиям сервиса.

    :param value: Значение email, которое передал пользователь
    :return: None
    """
    if RESTRICTED_EMAIL_DOMAIN in value:
        raise ValidationError(
            f"Your email domain is {RESTRICTED_EMAIL_DOMAIN}. Try to use another email."
        )

