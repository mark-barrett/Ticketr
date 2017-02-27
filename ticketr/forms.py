from django.contrib.auth.models import User
from models import Event, EventOwner, Category
from django import forms
from django.forms.widgets import Select


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

    event_owner = forms.ModelChoiceField(queryset=User.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CreateEventForm, self).__init__(*args, **kwargs)

        self.fields['event_owner'].queryset = EventOwner.objects.filter(owner=self.request.user)

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
                  'ticket1_price', 'ticket2_name', 'ticket2_price', 'ticket3_name', 'ticket3_price', 'location']


class CreateOrganiserProfileForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    website = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    facebook = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = EventOwner
        fields = ['name', 'description', 'website', 'facebook', 'image']
