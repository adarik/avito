import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from config import settings
from users.models import User, Location
from users.utils import return_one_user


class UserView(ListView):
    models = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        users = []
        for user in page_object:
            users.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'role': user.role,
                'age': user.age,
                'location': list(map(str, user.location.all())),
            })

        response = {
            'items': users,
            'total': paginator.count,
            'num_pages': paginator.num_pages,
        }

        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return return_one_user(self.object)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'location']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        user = User.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            password=data['password'],
            role=data['role'],
            age=data['age'],
        )

        for location_name in data['location']:
            location, _ = Location.objects.get_or_create(name=location_name)
            user.location.add(location)

        return return_one_user(user)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'location']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)

        self.object.first_name = data['first_name']
        self.object.last_name = data['last_name']
        self.object.username = data['username']
        self.object.password = data['password']
        self.object.age = data['age']

        for location_name in data['location']:
            location, _ = Location.objects.get_or_create(name=location_name)
            self.object.location.add(location)

        self.object.save()

        return return_one_user(self.object)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse(
            {
                'satus': 'ok'
            },
            status=200
        )
