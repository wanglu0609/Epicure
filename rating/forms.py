from django import forms  
from .models import Restaurant  
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username","email","password1","password2")

    def save(self, commit=True): #.save means we want commit the data to save in SQL
        user = super(NewUserForm, self).save(commit=False) # not commit yet
        user.email = self.cleaned_data['email']
        if commit:
            user.save() # finally, we can commit
        return user
        
class RestaurantForm(forms.ModelForm):  
    class Meta:  
        model = Restaurant  
        fields = ('name', 'Address','Phone')

class CompleteForm(forms.ModelForm):  
    class Meta:  
        model = Restaurant  
        fields = ('name', 'Address','Phone','res_ID') #,'image')