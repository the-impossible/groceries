# My Django imports
from django import forms

# My app imports
from OBMS_auth.models import Accounts
from OBMS_basics.models import Product

class AccountCreationForm(forms.ModelForm):
    fullname = forms.CharField(required=True,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'autofocus':'',
            'placeholder':'Full name',
        }
    ))

    email = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Email',
            'type':'email'
        }
    ))

    phone = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Phone',
            'type':'number'
        }
    ))

    password = forms.CharField(required=True, help_text='Password must contain at least 6 characters',
    widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Password ',
            'type':'Password',
        }
    ))

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError('Password too short, should be at least 6 characters!')

        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if Accounts.objects.filter(email=email).exists():
            raise forms.ValidationError('Email Address Already exist!')

        return email

    class Meta:
        model = Accounts
        fields = ('fullname', 'email', 'phone', 'password')

class EditAccountCreationForm(forms.ModelForm):
    fullname = forms.CharField(required=True, help_text='Please enter your Fullname',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'autofocus':'',
            'placeholder':'Full name',
        }
    ))

    email = forms.CharField(required=True,help_text='Email', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Email',
            'type':'email'
        }
    ))

    phone = forms.CharField(required=True,help_text='Phone Number', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Phone',
            'type':'number'
        }
    ))

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
                'class':'form-control',
                'type':'file',
                'accept':'image/png, image/jpeg'
            }
        ))

    class Meta:
        model = Accounts
        fields = ('fullname', 'email', 'phone', 'picture')

class BillingForm(forms.ModelForm):
    fullname = forms.CharField(required=True, help_text='Please enter your Fullname',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'autofocus':'',
            'placeholder':'Full name',
        }
    ))

    email = forms.CharField(required=True,help_text='Email', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Email',
            'type':'email'
        }
    ))

    phone = forms.CharField(required=True,help_text='Phone Number', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Phone',
            'type':'number'
        }
    ))

    address = forms.CharField(required=True,help_text='Delivery Address', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Shop Address',
        }
    ))

    class Meta:
        model = Accounts
        fields = ('fullname', 'email', 'phone', 'address')

class AddProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1 :
            raise forms.ValidationError('Quantity must be greater or equal to 1')
        return quantity

