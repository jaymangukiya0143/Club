# Generated by Django 3.1.4 on 2021-04-17 17:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Events', '0001_initial'),
        ('Amenities', '0001_initial'),
        ('Member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.CharField(max_length=250)),
                ('status', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(1)])),
                ('payment_for', models.TextField(choices=[('P', 'Membership Plan'), ('B', 'Amenity Booking'), ('E', 'Event Tickets')], max_length=1)),
                ('booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Amenities.bookings')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Member.member')),
                ('membership', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Member.membership')),
                ('ticket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Events.tickets')),
            ],
        ),
    ]
