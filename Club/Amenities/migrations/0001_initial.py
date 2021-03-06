# Generated by Django 3.1.4 on 2021-04-17 17:03

import Amenities.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('occupancy', models.PositiveIntegerField()),
                ('amenity_type', models.CharField(choices=[('A1', 'Amenity'), ('A2', 'Activity')], default='', max_length=8)),
                ('rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('image1', models.ImageField(upload_to=Amenities.models.upload_img_path)),
                ('image2', models.ImageField(upload_to=Amenities.models.upload_img_path)),
                ('image3', models.ImageField(upload_to=Amenities.models.upload_img_path)),
                ('image4', models.ImageField(upload_to=Amenities.models.upload_img_path)),
            ],
        ),
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booked_on', models.DateTimeField(auto_now_add=True)),
                ('from_date', models.DateField()),
                ('from_time', models.CharField(choices=[('M', 'Morning'), ('E', 'Evening')], default='', max_length=1)),
                ('to_date', models.DateField()),
                ('to_time', models.CharField(choices=[('M', 'Morning'), ('E', 'Evening')], default='', max_length=1)),
                ('no_of_slots', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('total', models.CharField(max_length=7)),
                ('status', models.BooleanField(default=False)),
                ('confirm', models.BooleanField(default=False)),
                ('amenity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Amenities.amenities')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Member.member')),
            ],
            options={
                'permissions': (('view_booking', 'Can view all the bookings'),),
            },
        ),
    ]
