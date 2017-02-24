from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.views.generic import View
from .forms import UserForm, UserLoginForm, CreateEventForm
from .models import *
from django import forms
from django.contrib import messages
from django.core.mail import send_mail

User = get_user_model()


def index(request):
    # Get the index.html template in the templates folder
    template = loader.get_template('index.html')
    context = {
        # We want all categories objects to be sent
        'categories': Category.objects.all(),
    }
    # Return the template as a HttpResponse
    return HttpResponse(template.render(context, request))


def event(request, id):
    # Get the index.html template in the templates folder
    template = loader.get_template('event.html')
    context = {
        # Get the event with the id passed as a parameter
        'event': Event.objects.get(id=id),
        'tickets': Ticket.objects.all().filter(event=id)
    }
    # Return the template as a HttpResponse
    return HttpResponse(template.render(context, request))


def logout_user(request):
    logout(request)
    messages.success(request, 'Thanks for stopping by, missing you already <3')
    return redirect('/home')


class CreateEventView(View):
    form_class = CreateEventForm
    template_name = 'create-event.html'

    def get(self, request):
        form = self.form_class(None)
        if request.user.is_authenticated:
            return render(request, self.template_name, {'form': form})
        else:
            messages.success(request, 'You have to login before you can create an event.')
            return redirect('/login')


class LoginUserFormView(View):
    form_class = UserLoginForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Hey %s welcome back, you are now logged in.' % username)
            return redirect('index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'register.html'

    # When data has to be sent using a get
    def get(self, request):
        # None = no user data as it stands
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # When data has been posted. Add to database
    def post(self, request):
        # request.POST is where all the posted data is kept
        form = self.form_class(request.POST)

        # Error check the form
        if form.is_valid():
            # Create object from form but don't save in the database
            user = form.save(commit=False)

            # cleaned data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # change the users password
            user.set_password(password)

            # save to database
            user.save()

            # returns user objects if the credentials are correct
            user = authenticate(username=username, password=password)

            """
            send_mail('Welcome to Ticketr',
                      'Thank you for registering your account with us, '
                      'we are more than certain you will love it here!',
                      'no-reply@ticketr.com',
                      [email],
                      fail_silently=False)
                      """

            # check if we got a user back
            if user is not None:

                # check if the user is banned/active etc
                if user.is_active:
                    # login the user and create the session
                    login(request, user)
                    # Refer to the user from here as request.user
                    messages.success(request, 'Registered successfully, you are now logged in!')
                    return redirect('index')

        return render(request, self.template_name, {'form': form})
