from django.contrib.admin import ModelAdmin, StackedInline, TabularInline
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from chapter_3.models import Seller, Vehicle, VehicleModel, Engine
from .forms import AddEngineForm, EngineForm, EngineSuperUserForm


@admin.register(Engine)
class EngineAdmin(ModelAdmin):
    '''
    Engine Admin Form
    '''
    # pass

    #form = EngineForm
    # inlines = [VehicleInline, ]

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            print(request.user)

            if request.user.is_superuser:
                return EngineSuperUserForm
            else:
                return EngineForm
        else:
            return AddEngineForm

        return super(EngineAdmin, self).get_form(request, obj, **kwargs)

    def delete_model(self, request, obj):
        print(obj.__dict__)

        print('Before Delete')
        # Code actions before delete here

        super().delete_model(request, obj)

        print('After Delete')
        # Code actions after delete here

    def save_model(self, request, obj, form, change):
        print(obj.__dict__)

        print('Before Save')
        # Code actions before save here

        super().save_model(request, obj, form, change)

        print('After Save')
        # Code actions after save here


# class SellerAdmin(ModelAdmin):
#     pass


class SellerAdmin(UserAdmin):
    # inlines = [VehiclesInline,]
    actions_on_bottom = True
    actions_selection_counter = True
    preserve_filters = False
    list_per_page = 20
    ordering = ('username',)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'name',
        'is_staff',
        'is_superuser',
    )
    list_display_links = (
        'username',
        'name',
    )
    list_editable = (
        'first_name',
        'last_name',
    )
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'name',
        'groups'
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'name',
        'email'
    )
    prepopulated_fields = {
        'username': ('first_name', 'last_name',)
    }
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password',
            ),
        }),
        (('Personal Info'), {'fields': (
            'first_name',
            'last_name',
            'name',
            'email',
        )}),
        (('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        (('Important Dates'), {'fields': ('last_login',
                                          'date_joined',
                                          )}),
        (('Vehicles'), {
            'description': ('Vehicles that this user isselling.'),
            'fields': (
                'vehicles',
            ),
        }),
    )


class VehicleInline(StackedInline):
    model = Vehicle
    extra = 1


# class VehiclesInline(TabularInline): #fOR MANYTOMANY
#     model = Seller.vehicles.through
#     extra = 1


class VehicleAdmin(ModelAdmin):
    pass


class VehicleModelAdmin(ModelAdmin):
    pass


# class EngineAdmin(ModelAdmin):
#     inlines = [VehicleInline, ]


admin.site.register(Seller, SellerAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleModel, VehicleModelAdmin)
# admin.site.register(Engine, EngineAdmin)
