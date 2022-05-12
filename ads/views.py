import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ad, Category
from ads.utils import return_one_ad, return_one_category
from users.models import User


def main_page(request):
    return JsonResponse({
        "status": "ok"
    })


class AdView(ListView):
    model = Ad
    queryset = Ad.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        ads = []
        for ad in self.object_list:
            ads.append(
                {
                    'id': ad.id,
                    'name': ad.name,
                    'author_id': ad.author_id,
                    'author': ad.author.first_name,
                    'price': ad.price,
                    'description': ad.description,
                    'is_published': ad.is_published,
                    'category_id': ad.category_id,
                    'image': ad.image.url if ad.image else None,
                }
            )

        return JsonResponse(ads, safe=False)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return return_one_ad(ad)


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "category"]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        author = get_object_or_404(User, data['author_id'])
        category = get_object_or_404(Category, data['category'])

        ad = Ad.objects.create(
            name=data["name"],
            author=author,
            price=data["price"],
            description=data["description"],
            is_published=data["is_published"],
            category=category,
        )

        return return_one_ad(ad)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)
        self.object.name = data['name']
        self.object.price = data['price']
        self.object.description = data['description']

        self.object.author = get_object_or_404(User, data["author_id"])  # TODO Не работает. Задал вопрос в СЛАК
        self.object.category = get_object_or_404(Category, data["category_id"])

        self.object.save()

        return return_one_ad(self.object)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get('image', None)
        self.object.save()

        return return_one_ad(self.object)


class CategoryView(ListView):
    model = Category
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for category in self.object_list:
            response.append(
                {
                    'id': category.id,
                    'name': category.name,
                }
            )
        return JsonResponse(response, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return return_one_category(category)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        category = Category.objects.create(
            name=data['name'],
        )
        return return_one_category(category)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)
        self.object.name = data['name']

        self.object.save()

        return return_one_category(self.object)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)
