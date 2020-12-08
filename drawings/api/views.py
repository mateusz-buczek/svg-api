from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from drawings.api.serializers import BodySerializer


class ProjectionCreateView(CreateAPIView):
    serializer_class = BodySerializer
    permission_classes = [AllowAny]
