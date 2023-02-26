
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from .views import SellersView, VehiclesView, VehicleView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='chapter_10/index.html')),

    path('all-vehicles/', VehiclesView.as_view(), name='all-vehicles'),
    path('all-sellers/', SellersView.as_view(), name='all-sellers'),
    path('vehicle/<int:id>/', VehicleView.as_view(), name='vehicle-detail'),
]