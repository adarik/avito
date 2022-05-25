from django.http import Http404
from rest_framework.permissions import BasePermission

from ads.models import Ad
from users.models import User


class AdEditPermission(BasePermission):
    message = 'NONONO'

    def has_permission(self, request, view):
        if request.user.role in [User.MODERATOR, User.ADMIN]:
            return True

        try:
            ad_object = Ad.objects.get(pk=view.kwargs['pk'])
        except Ad.DoesNotExist:
            raise Http404

        if ad_object.author_id == request.user.id:
            return True
        return False
