from django import forms
from .models import Amenities,Bookings

class AmenitiesForm(forms.ModelForm):
    class Meta:
        model = Amenities
        fields = ('name','description','occupancy','amenity_type','rate','image1','image2','image3','image4')
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control custom_div  '}),
            'description': forms.Textarea(attrs={'class': 'form-control custom_div  '}),
            'occupancy': forms.NumberInput(attrs={'class': 'form-control custom_div  '}),
            'amenity_type': forms.Select(attrs={'class': 'form-control custom_div  '}),
            'rate' : forms.TextInput(attrs={'class':'form-control custom_div  ','min':'100'}),
            # 'image1' : forms.ImageField(attrs={'class':'form-control'}),
            # 'image2': forms.ImageField(attrs={'class': 'form-control'}),
            # 'image3': forms.ImageField(attrs={'class': 'form-control'}),
            # 'image4': forms.ImageField(attrs={'class': 'form-control'})
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = "__all__"