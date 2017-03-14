from django.db.models import Sum
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
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib.staticfiles.templatetags.staticfiles import static

User = get_user_model()


def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawInlineImage('https://camo.githubusercontent.com/0c5cbab8bc8edb19b72a01d3bace2187e022d799/687474703a2f2f692e696d6775722e636f6d2f614d6f345261482e706e67', 40, 735, width=200, height=75)
    p.drawInlineImage(
        'http://i.imgur.com/nexc1Q6.png',
        300, 200, width=200, height=200)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


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


class MyEvents(View):
    template_name = loader.get_template('my-events.html')

    def get(self, request):
        if request.user.is_authenticated:

            # Check if the user has events. If they do return them, else return an notice
            if EventOwner.objects.filter(owner_id=request.user.id).count() > 0:

                # Get all organisers under this account
                organisers = EventOwner.objects.all().filter(owner=request.user.id)
                context = {
                    'events': Event.objects.all().filter(event_owner__in=organisers)
                }
                return HttpResponse(self.template_name.render(context, request))
            else:
                messages.success(request, "You don't have any events yet!")
        else:
            return redirect('/login')

    def post(self, request):
        search_query = request.POST['search']

        # Get all organisers under this account
        organisers = EventOwner.objects.all().filter(owner=request.user.id)
        search_context = {
            'search_events': Event.objects.all().filter(event_owner_id__in=organisers, name__contains=search_query)
        }

        if len(search_context) > 0:
            return HttpResponse(self.template_name.render(search_context, request))
        else:
            messages.warning(request, "Cannot find that event!")


class ManageEvent(View):
    template_name = loader.get_template('manage-event.html')

    def get(self, request, id):
        # Check if user is logged in
        if request.user.is_authenticated:
            # Check if the user has access to this event
            e = Event.objects.get(id=id)
            # Look at this again. Perhaps figure out another filter method
            eo = EventOwner.objects.get(owner_id=request.user.id, name=e.event_owner.name)
            ticketquantity = Ticket.objects.all().filter(event=e).aggregate(Sum('quantity'))
            sold_ticketquantity = Ticket.objects.all().filter(event=e).aggregate(Sum('quantity_sold'))

            percentage = (float(sold_ticketquantity['quantity_sold__sum']) / float(ticketquantity['quantity__sum']))
            percentage *= 100

            context = {
                # We want all categories objects to be sent
                'event': Event.objects.get(id=id),
                'ticketquantity': ticketquantity,
                'sold_ticketquantity': sold_ticketquantity,
                'percentage': percentage
            }

            if eo.owner==request.user:
                return HttpResponse(self.template_name.render(context, request))
            else:
                return redirect('/myevents')
        else:
            return redirect('/login')


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
        if 'select1' in privacy:
            privacy = 'Public'
        elif 'select2' in privacy:
            privacy = 'Private'
        elif 'select3' in privacy:
            privacy = 'Invite'

        # Figure out if they want to resell or not
        if 'select1' in resell:
            resell = 'Yes'
        else:
            resell = 'No'

        # Figure out if when they want to resell
        if 'select1' in resell_when:
            resell_when = 'No'
        elif 'select2' in resell_when:
            resell_when = 'Anytime'
        elif 'select3' in resell_when:
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

        while range < limit:
            ticket = Ticket(name=tickets[range+0]+"#ENAME-"+name+"#EVENT_ID-"+str(event_temp.id), price=tickets[range+1], quantity=tickets[range+2], event=event_temp)
            ticket.save()
            range += 3

        print "Hello"
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


class BuyTicket(View):
    template = loader.get_template('buy-ticket.html')

    def post(self, request):
        event_id = request.POST['event_id']
        ticket_id = request.POST['ticket_id']
        ticket_quantity = int(request.POST['ticket_quantity'])

        ticket = Ticket.objects.get(id=ticket_id)

        if ticket.quantity == ticket.quantity_sold:
            messages.warning(request, "Sorry, that ticket is sold out, choose another.")
            return redirect('/event/' + event_id)
        else:
            # Check to see if there is enough availible tickets
            if (ticket.quantity - ticket.quantity_sold) >= ticket_quantity:
                # First we need to add the ticket to the queue.
                # Generate a token
                while True:
                    token = Helper.token_generator(64, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                    try:
                        db_token = TicketQueue.objects.get(token=token)
                    except TicketQueue.DoesNotExist:
                        break

                # Now that we have a token, lets put a ticket in the queue for the user
                # replace part over there ----------> with qty variable)
                queued_ticket = TicketQueue(ticket=ticket, token=token, ticket_quantity=ticket_quantity)
                queued_ticket.save()

                '''
                Now that we have that done we can remove a ticket that is for sale by adding to the
                ticket sold value on the ticket model
                '''
                ticket.quantity_sold += ticket_quantity  # Replace with quantity variable
                ticket.save()

                # Now we need to get the quantity of the ticket to get the total and calculate some fees
                total = ticket_quantity * ticket.price
                fees = float(total / 100) * 2.00
                fees += ticket_quantity * 1.00

                context = {
                    'event': Event.objects.get(id=event_id),
                    'ticket': ticket,
                    'token': token,
                    'subtotal' : total,
                    'fees' : fees,
                    'quantity': ticket_quantity,
                    'total': fees+float(total)
                }
                return HttpResponse(self.template.render(context, request))
            else:
                messages.warning(request, "Sorry, that quantity of tickets is not availible")
                return redirect('/event/' + event_id)


    def get(self, request):
        return redirect('index')


class TicketTimeout(View):

    def get(self, request, queue_token):
        if queue_token is not None:
            # Get ticket on queue

            try:
                ticket = TicketQueue.objects.get(token=queue_token)
            except:
                messages.warning(request, "Your ticket was released for sale to the general public because the timer ran out.")
                return redirect('index')

            # Get the ticket from the database to say that there is an availible ticket
            db_ticket = Ticket.objects.get(id=ticket.ticket.id)
            db_ticket.quantity_sold -= ticket.ticket_quantity
            db_ticket.save()

            # Delete the queued ticket
            ticket.delete()
            return redirect('index')
        else:
            return redirect('index')


def organiser(request, id):
    template = loader.get_template('organiser.html')
    context = {
        # Get the event with the id passed as a parameter
        'organiser': EventOwner.objects.get(id=id),
        'events': Event.objects.all().filter(event_owner=id)
    }
    # Return the template as a HttpResponse
    return HttpResponse(template.render(context, request))

