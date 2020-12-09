from django.urls import path

from drawings.api.views import ProjectionCreateView

app_name = 'api'

urlpatterns = [
    path(r'projection', ProjectionCreateView.as_view(), name='projection'),
]
