import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad, Category
from ads.permissions import AdEditPermission
from ads.serializers import AdSerializer
from ads.utils import return_one_ad, return_one_category
from config import settings
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

        categories = request.GET.getlist('cat', None)
        if categories:
            self.object_list = self.object_list.filter(category_id__in=categories)

        text = request.GET.get('text', None)
        if text:
            self.object_list = self.object_list.filter(name__icontains=text)

        location = request.GET.get("location", None)
        if location:
            self.object_list = self.object_list.filter(author__location__name__icontains=location)

        price_from = request.GET.get('price_from', None)
        if price_from:
            self.object_list = self.object_list.filter(price__gte=price_from)

        price_to = request.GET.get('price_to', None)
        if price_to:
            self.object_list = self.object_list.filter(price__lte=price_to)

        self.object_list = self.object_list.select_related('author').order_by('-price')
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page', None)
        page_object = paginator.get_page(page_number)

        ads = []
        for ad in page_object:
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

        response = {
            'items': ads,
            'num_pages': paginator.num_pages,
            'total': paginator.count,
        }

        return JsonResponse(response, safe=False)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "category"]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        author = get_object_or_404(User, pk=data['author_id'])
        category = get_object_or_404(Category, pk=data['category_id'])

        ad = Ad.objects.create(
            name=data["name"],
            author=author,
            price=data["price"],
            description=data["description"],
            is_published=data["is_published"],
            category=category,
        )

        return return_one_ad(ad)


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, AdEditPermission]


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, AdEditPermission]


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

        self.object_list = self.object_list.order_by('name')
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page", None)
        page_object = paginator.get_page(page_number)

        categories = []
        for category in page_object:
            categories.append(
                {
                    'id': category.id,
                    'name': category.name,
                }
            )

        response = {
            'items': categories,
            'total': paginator.count,
            'num_pages': paginator.num_pages,
        }

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
