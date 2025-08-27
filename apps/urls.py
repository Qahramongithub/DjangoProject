from django.urls import path

from apps.views import HikvisionAccessControlAPIView

urlpatterns = [
    path('telegram', HikvisionAccessControlAPIView.as_view()),
]


