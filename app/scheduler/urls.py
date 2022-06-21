from django.urls import path

from scheduler.views.index import IndexView

app_name = 'scheduler'
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
