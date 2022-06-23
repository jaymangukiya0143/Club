from django import forms
from .models import Events

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ('name','description','amenity','from_date','to_date','capacity','price','image1')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control custom_div col-md-6 col-lg-6 '}),
            'description': forms.Textarea(attrs={'class': 'form-control custom_div col-md-6 col-lg-6'}),
            'amenity' : forms.Select(attrs={'class': 'form-control custom_div col-md-6 col-lg-6'}),
            'capacity' : forms.NumberInput(attrs={'class': 'form-control custom_div col-md-6 col-lg-6'}),
            'price': forms.NumberInput(attrs={'class': 'form-control custom_div col-md-6 col-lg-6'}),
        }