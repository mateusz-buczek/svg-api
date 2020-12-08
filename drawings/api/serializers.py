import svgwrite
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

    def validate(self, data):
        if len(data.get('projection_plane')) != 2:
            raise serializers.ValidationError(
                {'projection_plane': _("Projection plane must be exactly 2-characters long")}
            )

        if data.get('projection_plane').upper() not in settings.ALLOWED_PLANES:
            raise serializers.ValidationError(
                {'projection_plane': _(f"Wrong projection plane! Allowed planes: {settings.ALLOWED_PLANES}")}
            )

        return data

    def create(self, validated_data):
        geometry = validated_data.pop('geometry')
        body = Body.objects.create(**validated_data)
        for geo in geometry:
            Geometry.objects.create(**geo, body=body)
        return body

    def create_svg(self, validated_data):
        drawing = svgwrite.Drawing('output.svg', profile='full')
        plane = validated_data['projection_plane'].lower()
        geometry = validated_data.pop('geometry')
        minx = 0
        miny = 0
        maxx = 0
        maxy = 0
        iteration = 0
        for geo in geometry:
            x1 = geo[f'{plane[0]}1']
            x2 = geo[f'{plane[0]}2']
            y1 = geo[f'{plane[1]}1']
            y2 = geo[f'{plane[1]}2']
            drawing.add(drawing.rect(
                insert=(
                    x1,
                    y1,
                ),
                size=(
                    x2 - x1,
                    y2 - y1,
                ),
                **{
                    'fill': settings.SVG_FILL,
                    'stroke': settings.SVG_STROKE,
                }
            ))
            if x1 < minx or iteration == 0:
                minx = x1
            if x2 > maxx or iteration == 0:
                maxx = x2
            if y1 < miny or iteration == 0:
                miny = y1
            if y2 > maxy or iteration == 0:
                maxy = y2
            iteration += 1

        drawing.viewbox(
            minx=minx-settings.SVG_VIEWBOX_PADDING,
            miny=miny-settings.SVG_VIEWBOX_PADDING,
            width=maxx-minx+settings.SVG_VIEWBOX_PADDING*2,
            height=maxy-miny+settings.SVG_VIEWBOX_PADDING*2,
        )
        xml_as_string = drawing.tostring()
        return xml_as_string
