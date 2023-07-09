from django.urls import path

from .views import *


urlpatterns = [
    path("process_db",ProcessDB, name="process_db"),
    path('search_image/', searchImage, name='upload_image'),
]