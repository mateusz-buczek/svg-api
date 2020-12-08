from django.contrib.admin import ModelAdmin, register

from drawings.drawings.models import Body, Geometry


@register(Body)
class BodyAdmin(ModelAdmin):
    fields = (
        'projection_plane',
    )


@register(Geometry)
class GeometryAdmin(ModelAdmin):
    fields = (
        'body',
        'x1',
        'x2',
        'y1',
        'y2',
        'z1',
        'z2',
    )
