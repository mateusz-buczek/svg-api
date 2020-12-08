import json

from rest_framework import renderers


class SVGRenderer(renderers.BaseRenderer):
    media_type = '*/*'
    format = 'svg'

    def render(self, data, media_type=None, renderer_context=None):
        if renderer_context['response'].status_code == 400:
            return json.dumps(data)
        return data
