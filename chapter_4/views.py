from django.template.response import (
    TemplateResponse
)
from chapter_3.models import Vehicle
from django.http import Http404


def practice_view(request, year):
    return TemplateResponse(
        request, 'chapter_4/my_practice_page.html',
        {'year': year}
    )


def practice_year_view(request, year):
    if year >= 1900:
        return TemplateResponse(
            request,
            'chapter_4/my_year.html',
            {'year': year}
        )
    else:
        raise Http404(f'Year Not Found: {year}')


def vehicle_view(request, id):
    try:
        vehicle = Vehicle.objects.get(id=id)
    except Vehicle.DoesNotExist:
        raise Http404(f'Vehicle ID Not Found: {id}')
    return TemplateResponse(
        request,
        'chapter_4/my_vehicle.html',
        {'vehicle': vehicle}
    )
