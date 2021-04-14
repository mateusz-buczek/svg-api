import svgwrite
from django.conf import settings
from django.db import models


class Body(models.Model):
    projection_plane = models.CharField(max_length=2)

    def create_svg(self):
        drawing = svgwrite.Drawing('output.svg', profile='full')
        plane = self.projection_plane.lower()
        minx, miny, maxx, maxy = None, None, None, None

        for geo in self.geometry.all():
            x1 = getattr(geo, f'{plane[0]}1')
            x2 = getattr(geo, f'{plane[0]}2')
            y1 = getattr(geo, f'{plane[1]}1')
            y2 = getattr(geo, f'{plane[1]}2')
            drawing.add(drawing.rect(
                insert=(x1, y1),
                size=(x2 - x1, y2 - y1),
                fill=settings.SVG_FILL,
                stroke=settings.SVG_STROKE,
            ))
            if minx is None or x1 < minx:
                minx = x1
            if maxx is None or x2 > maxx:
                maxx = x2
            if miny is None or y1 < miny:
                miny = y1
            if maxy is None or y2 > maxy:
                maxy = y2

        drawing.viewbox(
            minx=minx-settings.SVG_VIEWBOX_PADDING,
            miny=miny-settings.SVG_VIEWBOX_PADDING,
            width=maxx-minx+settings.SVG_VIEWBOX_PADDING*2,
            height=maxy-miny+settings.SVG_VIEWBOX_PADDING*2,
        )
        return drawing.tostring()


class Geometry(models.Model):
    body = models.ForeignKey(
        'Body',
        related_name='geometry',
        on_delete=models.CASCADE,
    )
    x1 = models.IntegerField()
    x2 = models.IntegerField()
    y1 = models.IntegerField()
    y2 = models.IntegerField()
    z1 = models.IntegerField()
    z2 = models.IntegerField()
