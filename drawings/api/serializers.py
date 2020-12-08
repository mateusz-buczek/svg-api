from django.conf import settings
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from drawings.drawings.models import Body, Geometry


class GeometrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Geometry
        exclude = [
            'body',
            'id',
        ]


class BodySerializer(serializers.ModelSerializer):
    geometry = GeometrySerializer(many=True)

    class Meta:
        model = Body
        fields = '__all__'
        depth = 2

    def validate(self, data):
        if len(data.get('projection')) != 2:
            raise serializers.ValidationError(
                {'projection': _("Projection must be exactly 2-characters long")}
            )

        if data.get('projection').upper() not in settings.ALLOWED_PLANES:
            raise serializers.ValidationError(
                {'projection': _(f"Wrong plane! Allowed planes: {settings.ALLOWED_PLANES}")}
            )

        return data
