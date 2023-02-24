from django.urls import re_path
from django.views.generic import (
    TemplateView
)
from .views import FormClassView, ModelFormClassCreateView, ModelFormClassUpdateView


urlpatterns = [
    re_path(
        r'^chapter-5/form-class/?$',
        FormClassView.as_view()
    ),

    re_path(
        r'^chapter-5/contact-form-success/?$',
        TemplateView.as_view(
            template_name='chapter_5/contact-success.html'
        ),
        kwargs={
            'title': 'FormClassView Success Page',
            'page_id': 'form-class-success',
            'page_class': 'form-class-success-page',
            'h1_tag': 'This is the FormClassView Success Page Using ContactForm',
        }
    ),
    re_path(
        r'^chapter-5/model-form-class/?$',
        ModelFormClassCreateView.as_view()
    ),
    re_path(
        r'^chapter-5/vehicle-form-success/?$',
        TemplateView.as_view(
            template_name='chapter_5/vehicle-success.html'
        ),
        kwargs={
            'title': 'ModelFormClass Success Page',
            'page_id': 'model-form-class-success',
            'page_class': 'model-form-class-successpage',
            'h1_tag': 'This is the ModelFormClass Success Page Using VehicleForm',
        }
    ),
    re_path(
        'chapter-5/model-form-class/(?P<id>[0-9])/?$',
        ModelFormClassUpdateView.as_view(),
        name='vehicle_detail'
    ),
]
