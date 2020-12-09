from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drawings.api.renderers import SVGRenderer
from drawings.api.serializers import BodySerializer


class ProjectionCreateView(CreateAPIView):
    serializer_class = BodySerializer
    permission_classes = [AllowAny]
    renderer_classes = [SVGRenderer]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.create_svg(serializer.validated_data)
            return Response(data, status=status.HTTP_200_OK, content_type='image/svg+xml')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
