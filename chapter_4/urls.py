from django.urls import path, register_converter
from django.views.generic import TemplateView, RedirectView
from .converters import YearConverter
from .views import practice_view, practice_year_view, vehicle_view

register_converter(YearConverter, 'year')

urlpatterns = [
    path('chapter-4/', TemplateView.as_view(
        template_name='chapter_4/chapter_4.html')
    ),
    path('my_path/my_unwanted_url/', RedirectView.as_view(
        url='http://localhost:8000/my_wanted_url/', permanent=True)
    ),
    # path('my_year_path/<year:year>/', practice_view),
    path('my_year_path/<year:year>/', practice_year_view, name='year_url'),
    path('vehicle/<int:id>/', vehicle_view, name='vehicle-detail'),
]
