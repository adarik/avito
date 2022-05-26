from django.http import Http404
from rest_framework.permissions import BasePermission

from ads.models import Ad, Selection
from users.models import User


class AdEditPermission(BasePermission):
    message = "You don't have permissions for that :("

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


class SelectionEditPermission(BasePermission):
    message = "You don't have permissions for that :("

    def has_permission(self, request, view):
        try:
            select_object = Selection.objects.get(pk=view.kwargs['pk'])
        except Selection.DoesNotExist:
            raise Http404

        if select_object.owner_id == request.user.id:
            return True
        return False
