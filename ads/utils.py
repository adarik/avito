from django.http import JsonResponse


def return_one_ad(ad):
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


def return_one_category(category):
    return JsonResponse({
        'id': category.id,
        'name': category.name,
    })
