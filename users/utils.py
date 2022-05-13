from django.http import JsonResponse

from users.models import User


def return_one_user(user: User) -> JsonResponse:
    """
    Функция выдачи во вьюшке одного пользователя

    :param user: Пользователь, полученный из БД
    :return: JsonResponse Django
    """
    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "age": user.age,
        "locations": list(map(str, user.location.all())),
    })
