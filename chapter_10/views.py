''' Chapter 10 Views Module '''
#from django.db.models import Prefetch
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic import View

from chapter_3.models import Seller, Vehicle


class SellersView(View):
    '''
    Sellers View - Maps to http://localhost:8000/all-sellers/
    '''
    template_name = 'chapter_10/sellers.html'

    def get(self, request, *args, **kwargs):
        '''
        GET Method for SellersView
        '''
        try:
            sellers = Seller.objects.all()  # Produces 19 Queries

            # Produces 4 Queries (1 for Seller, 1 for Vehicle, 1 for Vehicle_Modle, 1 for Engine)
            # sellers = Seller.objects.prefetch_related(
            #    'vehicles',
            #    'vehicles__vehicle_model',
            #    'vehicles__engine'
            # ).all()

            # Produces 4 Queries (1 for Seller, 1 for Vehicle, 1 for Vehicle_Modle, 1 for Engine)
            # and Filters the related Vehicles
            # sellers = Seller.objects.prefetch_related(
            #    Prefetch(
            #        'vehicles',
            #        to_attr  = 'filtered_vehicles',
            #        queryset = Vehicle.objects.filter(vehicle_model__name='Blazer LT')
            #    ),
            #    'filtered_vehicles__vehicle_model',
            #    'filtered_vehicles__engine'
            # ).all()

            # Extra-Extra Practice
            # sellers = Seller.objects.prefetch_related(
            # 'groups',
            # 'user_permissions',
            # 'vehicles',
            # 'vehicles__vehicle_model',
            # 'vehicles__engine'
            # ).all()
            # sellers = Seller.objects.select_related(
            # 'auth_token'
            # ).prefetch_related(
            # 'groups',
            # 'user_permissions',
            # 'vehicles',
            # 'vehicles__vehicle_model',
            # 'vehicles__engine'
            # ).all()
        except Seller.DoesNotExist:
            raise Http404('No Sellers Found')

        return TemplateResponse(request, self.template_name, {'sellers': sellers})


class VehiclesView(View):
    '''
    Vehicles View - Maps to http://localhost:8000/all-vehicles/
    '''
    template_name = 'chapter_10/vehicles.html'

    def get(self, request, *args, **kwargs):
        '''
        GET Method for VehiclesView
        '''
        try:
            # Produces 15 Queries
            vehicles = Vehicle.objects.all()

            # Produces 1 Query
            # vehicles = Vehicle.objects.select_related(
            #    'vehicle_model',
            #    'engine'
            # ).all()

            # Use After Adding {% for seller in vehicle.vehicle_sellers.all %} in vehicles.html
            # Same Query As Before, Now Produces 8 Queries Instead of 1
            # vehicles = Vehicle.objects.select_related(
            #    'vehicle_model',
            #    'engine'
            # ).all()
            # Produces 2 Queries
            # vehicles = Vehicle.objects.prefetch_related(
            #    'vehicle_sellers'
            # ).select_related(
            #    'vehicle_model',
            #    'engine'
            # ).all()
        except Vehicle.DoesNotExist:
            raise Http404('No Vehicles Found')

        return TemplateResponse(request, self.template_name, {'vehicles': vehicles})


# Extra Practice - Vehicle Detail View
class VehicleView(View):
    '''
    Vehicle View (Single Object) - Maps to http://localhost:8000/vehicle/#/
    '''
    template_name = 'chapter_10/vehicle.html'

    def get(self, request, id, *args, **kwargs):
        '''
        GET Method for VehicleView
        '''
        try:
            # Produces 3 Queries
            vehicle = Vehicle.objects.get(id=id)

            # Produces 1 Query
            vehicle = Vehicle.objects.select_related(
                'vehicle_model',
                'engine'
            ).get(id=id)

        except Vehicle.DoesNotExist:
            raise Http404(f'Vehicle ID Not Found: {id}')

        return TemplateResponse(request, self.template_name, {'vehicle': vehicle})
