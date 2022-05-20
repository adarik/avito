from django.http import JsonResponse

from ads.models import Category, Ad


def return_one_ad(ad: Ad) -> JsonResponse:
    """
    Функция выдачи во вьюшке одного объявления
    :param ad: Полученное из БД объявление
    :return: JsonResponse Django
    """
    return JsonResponse(
        {
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.first_name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None,
        }
    )


def return_one_category(category: Category) -> JsonResponse:
    """
    Функция выдачи во вьюшке одной категории
    :param category: Категория, полученная из БД
    :return: JsonResponse Django
    """
    return JsonResponse({
        'id': category.id,
        'name': category.name,
    })
