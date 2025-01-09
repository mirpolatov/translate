from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path('', views.translator_view, name='translator'),  # Add this line
    # other url patterns...
]
