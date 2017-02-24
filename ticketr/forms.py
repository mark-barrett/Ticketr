from django.contrib.auth.models import User
from models import Event
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        # if you want unique email address. else delete this function
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("This email address is already in use. Please supply a different email address.")
        return self.cleaned_data['email']


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class CreateEventForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    ticket1_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    ticket1_price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    ticket2_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    ticket2_price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    ticket3_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    ticket3_price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Event
        fields = ['name', 'image', 'description', 'category', 'event_owner', 'ticket1_name',
                  'ticket1_price', 'ticket2_name', 'ticket3_name', 'ticket3_price', 'location']


