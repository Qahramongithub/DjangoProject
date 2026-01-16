from django.urls import path

from apps.views import HikEventView

urlpatterns = [
    path('telegram', HikEventView.as_view()),
]


