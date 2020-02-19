from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Information,Reviews

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

class InformationForm(forms.ModelForm):

    class Meta:
        model = Information 
        fields = ['FirstName','Major','Gender','Favorite_Cuision','Favorite_Restaurant']

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Reviews 
        fields = ['rating','comment']