# Generated by Django 4.0 on 2023-02-22 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chapter_3', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='make',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Buick'), (2, 'Cadillac'), (3, 'Chevrolet')], null=True, verbose_name='Vehicle Make/Brand'),
        ),
    ]