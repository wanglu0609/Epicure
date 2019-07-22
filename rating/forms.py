from django import forms  
from .models import Restaurant  
class RestaurantForm(forms.ModelForm):  
    class Meta:  
        model = Restaurant  
        fields = ('name', 'Address','Phone')

class CompleteForm(forms.ModelForm):  
    class Meta:  
        model = Restaurant  
        fields = ('name', 'Address','Phone','res_ID')