from django import forms
from .models import Plans

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plans
        fields = "__all__"
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control col-md-6 col-lg-6','style':'margin-bottom:10px'}),
            'description' : forms.Textarea(attrs={'class':'form-control col-md-6 col-lg-6','style':'margin-bottom:10px'}),
            'duration' : forms.NumberInput(attrs={'class':'form-control col-md-6 col-lg-6','placeholder':'in months','style':'margin-bottom:10px'}),
            'fees' : forms.NumberInput(attrs={'class':'form-control col-md-6 col-lg-6','min':'100'}),
        }