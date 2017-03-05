from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.views.generic import View
from .forms import UserForm, UserLoginForm, CreateEventForm, CreateOrganiserProfileForm
from .models import *
from django import forms
from django.contrib import messages
from django.core.mail import send_mail
from datetime import datetime
from helper import *

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
        form = self.form_class(request)
        if request.user.is_authenticated:

            # Now check to make sure the user has created an "Event Organiser" name
            eo = EventOwner.objects.filter(owner_id=request.user.id)

            # If there has been an event owner made
            if eo.count() > 0:
                return render(request, self.template_name, {'form': form})

            # Else send the user to the create event owner
            else:
                messages.warning(request, 'You must have an organiser profile setup before creating an event.')
                return redirect('/create-organiser')
        else:
            messages.success(request, 'You have to login before you can create an event.')
            return redirect('/login')

    def post(self, request):
        name = request.POST['name']
        location = request.POST['location']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        image = request.POST['image']
        description = request.POST['description']
        category = request.POST['category']
        event_owner = request.POST['event_owner']
        ticket1_name = request.POST['ticket1_name']
        ticket2_name = request.POST['ticket2_name']
        ticket3_name = request.POST['ticket3_name']
        ticket1_price = request.POST['ticket1_price']
        ticket2_price = request.POST['ticket2_price']
        ticket3_price = request.POST['ticket3_price']
        ticket1_qty = request.POST['ticket1_qty']
        ticket2_qty = request.POST['ticket2_qty']
        ticket3_qty = request.POST['ticket3_qty']
        privacy = request.POST['privacy']
        resell = request.POST['resell']
        resell_when = request.POST['resell_when']
        resell_amount = request.POST['resell_amount']

        # Check if privacy is set to which and make appropriate changes
        if 'Public' in privacy:
            privacy = 'Public'
        elif 'Private' in privacy:
            privacy = 'Private'
        else:
            privacy = 'Invite'

        # Figure out if they want to resell or not
        if 'Yes' in resell:
            resell = 'Yes'
        else:
            resell = 'No'

        # Figure out if when they want to resell
        if 'no' in resell_when:
            resell_when = 'No'
        elif 'anytime' in resell_when:
            resell_when = 'Anytime'
        elif 'out' in resell_when:
            resell_when = 'Sell Out'
        else:
            resell_when = 'Amount'

        # Figure out how many tickets they want sold before sale if set
        if resell_amount is None:
            resell_amount = 'No'

        event_category = Category.objects.get(id=category)
        event_owner_object = EventOwner.objects.get(id=event_owner)

        event_temp = Event(name=name, image=image, description=description, location=location, start_date=Helper.date(start_date),
                           start_time=start_time, end_date=Helper.date(end_date), end_time=end_time, event_owner=event_owner_object,
                           category=event_category, privacy=privacy, resell=resell, resell_when=resell_when,
                           resell_amount=resell_amount)

        event_temp.save()

        limit = 3
        # Now the tickets
        tickets = [ticket1_name, ticket1_price, ticket1_qty]

        if ticket1_name is not None:
            tickets.append(ticket2_name)
            tickets.append(ticket2_price)
            tickets.append(ticket2_qty)
            limit = 6
        if ticket2_name is not None:
            tickets.append(ticket3_name)
            tickets.append(ticket3_price)
            tickets.append(ticket3_qty)
            limit = 9

        range = 0
        print tickets
        while range < limit:
            ticket = Ticket(name=tickets[range+0], price=tickets[range+1], quantity=tickets[range+2], event=event_temp)
            ticket.save()
            range += 3

        if event is not None:
            messages.success(request, "Nice one! Your event created successfully.")
            return redirect(index)


class CreateOrganiserView(View):
    form_class = CreateOrganiserProfileForm
    template_name = 'create-organiser.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        name = request.POST['name']
        description = request.POST['description']
        website = request.POST['website']
        facebook = request.POST['facebook']
        image = request.POST['image']

        eo = EventOwner(name=name, description=description, website=website, facebook=facebook, image=image,
                        owner=request.user)

        eo.save()

        if eo is not None:
            messages.success(request, "Created organiser profile successfully!")
            return redirect('index')


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


class OrganiserProfiles(View):

    def get(self, request):
        eo = EventOwner.objects.filter(owner_id=request.user.id)

        # Check if there are profiles
        if eo.count() > 0:
            # Profiles exists
            template = loader.get_template('organiser-profiles.html')
            context = {
                'profiles': EventOwner.objects.all().filter(owner=request.user)
            }
            return HttpResponse(template.render(context, request))
        else:
            # If no profiles have been created
            messages.warning(request, 'You do not have any organiser profiles. Create one first.')
            return redirect('/create-organiser')


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
