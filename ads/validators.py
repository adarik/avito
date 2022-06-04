from rest_framework import serializers


class NotTrueValidator:
    def __call__(self, value):
        if value:
            raise serializers.ValidationError("New ad can not be published")
