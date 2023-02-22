from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from django.db.models.functions import Lower

MAKE_CHOICES = (
    (1, 'Buick'),
    (2, 'Cadillac'),
    (3, 'Chevrolet'),
)

YESNO_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class VehicleModel(models.Model):
    name = models.CharField(
        verbose_name='Model',
        max_length=75,
        unique=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Vehicle Model'
        verbose_name_plural = 'Vehicle Models'
        ordering = ['-name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(
                fields=['-name'],
                name='desc_name_idx'
            ),
            models.Index(
                Lower('name').desc(),
                name='lower_name_idx'
            )
        ]


class Engine(models.Model):
    name = models.CharField(
        verbose_name='Engine',
        max_length=75,
        blank=True,
        null=True,
    )
    vehicle_model = models.ForeignKey(
        VehicleModel,
        on_delete=models.CASCADE,
        verbose_name='Model',
        related_name='model_engine',
        blank=True,
        null=True,
    )


class Vehicle(models.Model):
    vin = models.CharField(
        verbose_name='VIN',
        max_length=17,
        unique=True,
        blank=True,
        null=True,
    )
    sold = models.BooleanField(
        verbose_name='Sold?',
        choices=YESNO_CHOICES,
        default=False,
        blank=True,
        null=True,
    )

    price = MoneyField(
        max_digits=19,
        decimal_places=2,
        default_currency='USD',
        null=True,
        validators=[
            MinMoneyValidator(
                {'EUR': 500, 'USD': 400}
            ),
            MaxMoneyValidator(
                {'EUR': 500000, 'USD': 400000}
            ),
        ])
    vehicle_model = models.ForeignKey(
        VehicleModel,
        on_delete=models.CASCADE,
        verbose_name='Model',
        related_name='model_vehicle',
        blank=True,
        null=True,
    )
    engine = models.ForeignKey(
        Engine,
        on_delete=models.CASCADE,
        verbose_name='Engine',
        related_name='engine_vehicle',
        blank=True,
        null=True,
    )
    make = models.PositiveIntegerField(
        choices=MAKE_CHOICES,
        verbose_name='Vehicle Make/Brand',
        blank=True,
        null=True,
    )


class Seller(models.Model):
    name = models.CharField(
        verbose_name='Seller Name',
        max_length=150,
        blank=True,
        null=True,
    )

    vehicle = models.ManyToManyField(
        Vehicle,
        verbose_name='Vehicles',
        related_name='vehicle_sellers',
        related_query_name='vehicle_seller',
        blank=True,
    )


class engine2(models.Model):
    name = models.CharField(
        verbose_name='Engine', max_length=75,
        blank=True, null=True,
    )

    class Meta:
        db_table = 'chapter_3_practice_engine'
