
from django.contrib.auth.models import User
from django import forms

from .models import Stores, Listings, Cart


class AddStore(forms.ModelForm):

    class Meta():
        model = Stores
        fields = ("store_name","address")



class AddListings(forms.ModelForm):


    class Meta():

        model = Listings
        exclude = ('store',)



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class AddCart(forms.ModelForm):

    class Meta():
        model = Cart

        fields = "__all__"