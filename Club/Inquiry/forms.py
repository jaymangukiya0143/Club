from .models import *
from django import forms


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ('name','email','phone','subject','message')
        widgets={
            'name' : forms.TextInput(attrs={'class':'form-control custom_div'}),
            'email' : forms.TextInput(attrs={'class':'form-control custom_div'}),
            'phone' : forms.TextInput(attrs={'class':'form-control custom_div'}),
            'subject' : forms.TextInput(attrs={'class':'form-control custom_div'}),
            'message' : forms.Textarea(attrs={'class':'form-control custom_div'})
        }