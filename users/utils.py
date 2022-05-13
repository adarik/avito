from django.http import JsonResponse


def return_one_user(user):
    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "age": user.age,
        "locations": list(map(str, user.location.all())),
    })
