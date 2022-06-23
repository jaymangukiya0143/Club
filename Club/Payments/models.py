from django.db import models
from Plans.models import Plans
from Amenities.models import Bookings
from Member.models import Member,Membership
from Events.models import Events,Tickets
from django.core.validators import MinValueValidator

# Create your models here.

Payment_For=(
    ('P','Membership Plan'),
    ('B','Amenity Booking'),
    ('E','Event Tickets')
)

class Payments(models.Model):
    membership = models.ForeignKey(Membership,on_delete=models.CASCADE,null=True,blank=True)
    booking = models.ForeignKey(Bookings,on_delete=models.CASCADE,null=True,blank=True)
    member = models.ForeignKey(Member,on_delete=models.CASCADE,null=True,blank=True)
    ticket = models.ForeignKey(Tickets,on_delete=models.CASCADE,null=True,blank=True)
    invoice_id = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(default=0.00,max_digits=10,decimal_places=2,validators=[MinValueValidator(1)])
    payment_for = models.TextField(choices=Payment_For,max_length=1)

    def __str__(self):
        return self.payment_for + ' - ' + self.invoice_id