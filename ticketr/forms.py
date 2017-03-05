from django.contrib.auth.models import User
from models import Event, EventOwner, Category
from django import forms
from django.forms.widgets import Select
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div
from functools import partial
from django.conf import settings


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-xs', 'placeholder': 'Password'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xs', 'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xs', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        # if you want unique email address. else delete this function
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("This email address is already in use. Please supply a different email address.")
        return self.cleaned_data['email']


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-xs', 'placeholder': 'Password'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xs', 'placeholder': 'Username'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class CreateEventForm(forms.ModelForm):
    DateInput = partial(forms.DateInput, {'class': 'datepicker'})

    event_owner = forms.ModelChoiceField(queryset=User.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control input-xs'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control input-xs'}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CreateEventForm, self).__init__(*args, **kwargs)

        self.fields['event_owner'].queryset = EventOwner.objects.filter(owner=self.request.user)
        self.fields['name'].label = "Event Name"
        self.fields['event_owner'].label = "Event Owner/Organiser"
        self.fields['category'].label = "Event Type:"
        self.fields['ticket1_name'].label = "Ticket Name"
        self.fields['ticket2_name'].label = "Ticket Name"
        self.fields['ticket3_name'].label = "Ticket Name"
        self.fields['ticket1_price'].label = "Ticket Price"
        self.fields['ticket2_price'].label = "Ticket Price"
        self.fields['ticket3_price'].label = "Ticket Price"
        self.fields['ticket1_qty'].label = "Ticket Quantity"
        self.fields['ticket2_qty'].label = "Ticket Quantity"
        self.fields['ticket3_qty'].label = "Ticket Quantity"
        self.fields['privacy'].label = "Event Privacy"
        self.fields['resell'].label = "Would you like event goers to be able to re-sell their tickets on Ticketr?"
        self.fields['resell_when'].label = "If so, when should they be able to sell them?"
        self.fields['resell_amount'].label = "If choosen above, how many tickets should be sold before re-selling can occur?"

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xs'}))
    image = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xs'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control input-xs'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xs'}))
    start_date = forms.DateField(widget=DateInput(), input_formats=settings.DATE_INPUT_FORMATS)
    start_time = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control input-xxs'}))
    end_date = forms.DateField(widget=DateInput(), input_formats=settings.DATE_INPUT_FORMATS)
    end_time = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control input-xxs'}))

    ticket1_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xs'}))
    ticket1_price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xxs'}))
    ticket1_qty = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xxs'}))
    ticket2_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xs'}))
    ticket2_price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xxs'}))
    ticket2_qty = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xxs'}))
    ticket3_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xs'}))
    ticket3_price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xxs'}))
    ticket3_qty = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xxs'}))

    PRIVACYCHOICES = [('select1', 'Public - List your event for anybody to see on the Ticketr website.'),
               ('select2', 'Private - Do not list this event. Only people with a link can view.'),
               ('select3', 'Invite Only - Only people who have an invite code can buy tickets.')]

    RESELLCHOICES = [('select1', 'Yes! - I want to allow event goers to re-sell their tickets'),
                     ('select2', 'No! - I do not want event goers to be able to re-sell tickets')]

    RESELLWHENCHOICES = [('select1', 'I choose no above'),
                         ('select2', 'Allow event goers to re-sell tickets at anytime'),
                         ('select3', 'Allow event goers to re-sell tickets once the event has sold out'),
                         ('select1', 'Allow event goers to re-sell after a certain amount of tickets have been sold.')]

    privacy = forms.ChoiceField(choices=PRIVACYCHOICES, widget=forms.Select(attrs={'class': 'form-control input-xs'}))
    resell = forms.ChoiceField(choices=RESELLCHOICES, widget=forms.Select(attrs={'class': 'form-control input-xs'}))
    resell_when = forms.ChoiceField(choices=RESELLWHENCHOICES, widget=forms.Select(attrs={'class': 'form-control input-xs'}))
    resell_amount = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-xxs'}))

    class Meta:
        model = Event
        fields = ['name', 'location', 'start_date', 'end_date', 'start_time', 'end_time', 'image', 'description', 'category', 'event_owner', 'ticket1_name',
                  'ticket1_price', 'ticket1_qty', 'ticket2_name', 'ticket2_price', 'ticket2_qty', 'ticket3_name',
                  'ticket3_price', 'ticket3_qty', 'privacy', 'resell', 'resell_when', 'resell_amount']


class CreateOrganiserProfileForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    website = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    facebook = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = EventOwner
        fields = ['name', 'description', 'website', 'facebook', 'image']
