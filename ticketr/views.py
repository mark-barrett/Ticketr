from decimal import Decimal
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
import datetime
from helper import *
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
import qrcode
import StringIO
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from pathlib import Path
from reportlab.lib.units import inch

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

    event = Event.objects.get(id=id)

    context = {
        # Get the event with the id passed as a parameter
        'event': event,
        'tickets': Ticket.objects.all().filter(event=id),
        'resells': ResellList.objects.all().filter(event=event)
    }
    # Check if the event is over or not
    event_end_time_date = datetime.datetime.combine(event.end_date, event.end_time)

    if event_end_time_date < datetime.datetime.now():
        messages.warning(request, 'Sorry that event is over!')
        return redirect('index')
    else:
        # Return the template as a HttpResponse
        return HttpResponse(template.render(context, request))


def logout_user(request):
    logout(request)
    messages.success(request, 'Thanks for stopping by, missing you already <3')
    return redirect('/home')


class MyTickets(View):
    template_name = loader.get_template('my-tickets.html')


    def get(self, request):
        # Check if the user is authenticated. They must be in order to view their tickets
        if request.user.is_authenticated:

            context = {
                'tickets' : Order.objects.all().filter(user=request.user)
            }
            return HttpResponse(self.template_name.render(context, request))


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
                'percentage': percentage,
                'orders': Order.objects.all().filter(event=e)
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


class DownloadTicket(View):

    def get(self, request, order_number):
        if request.user.is_authenticated:
            # Check the ticket exists
            try:
                order = Order.objects.get(order_number=order_number)
                # Check if the user who is logged in owns this ticket
                if order.user == request.user:

                    # Check if the file exists
                    qr_path = Path('qrcode/qr-'+order_number+'.png')
                    if qr_path.is_file():
                        # Generate PDF Here if it doesnt exist

                        # Create the HttpResponse object with the appropriate PDF headers.
                        response = HttpResponse(content_type='application/pdf')
                        response['Content-Disposition'] = 'attachment; filename="order-'+order_number+'.pdf"'

                        # Create the PDF object, using the response object as its "file."
                        p = canvas.Canvas(response)

                        # Draw things on the PDF. Here's where the PDF generation happens.
                        # See the ReportLab documentation for the full list of functionality.
                        p.drawInlineImage(
                            'images/newticket.png',
                            0, 0, width=600, height=850)

                        # Draw details onto the pdf
                        p.setFont("Helvetica", 15)
                        p.drawString(48, 330, order.event.name)
                        p.setFont("Helvetica", 12)

                        # Event location
                        p.drawString(315, 265, order.event.location)

                        # Add order details
                        p.drawString(48, 180, "Order number "+order.order_number+" purchased by "+order.user.username)

                        # Add date
                        p.drawString(48, 265, (str(order.event.start_date)) + " @ " + (str(order.event.start_time)))

                        # Ticket type
                        p.drawString(315, 180, Helper.remove_key(order.ticket.name, "#ENAME"))

                        # Add QRCode
                        p.drawInlineImage('qrcode/qr-'+order_number+'.png', 370, 415, width=140, height=140)

                        # Close the PDF object cleanly, and we're done.
                        p.showPage()
                        p.save()
                        return response
                    else:
                        qr = qrcode.QRCode(version=1,
                                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                                           box_size=6,
                                           border=0)
                        qr.add_data(order.order_code)
                        qr.make(fit=True)

                        img = qr.make_image()

                        buffer = StringIO.StringIO()
                        img.save(buffer)
                        filename = 'qr-%s.png' % (order_number)
                        filebuffer = InMemoryUploadedFile(
                            buffer, None, filename, 'images/qr_codes/png', buffer.len, None)

                        order.qrcode.save(filename, filebuffer)

                        # Generate the pdf now that it does exist
                        # Create the HttpResponse object with the appropriate PDF headers.
                        response = HttpResponse(content_type='application/pdf')
                        response['Content-Disposition'] = 'attachment; filename="order-'+order_number+'.pdf"'

                        # Create the PDF object, using the response object as its "file."
                        p = canvas.Canvas(response)

                        # Draw things on the PDF. Here's where the PDF generation happens.
                        # See the ReportLab documentation for the full list of functionality.
                        p.drawInlineImage(
                            'images/newticket.png',
                            0, 0, width=600, height=850)

                        # Draw details onto the pdf
                        p.setFont("Helvetica", 15)
                        p.drawString(48, 330, order.event.name)
                        p.setFont("Helvetica", 12)

                        # Event location
                        p.drawString(315, 265, order.event.location)

                        # Add order details
                        p.drawString(48, 180,
                                     "Order number " + order.order_number + " purchased by " + order.user.username)

                        # Add date
                        p.drawString(48, 265, (str(order.event.start_date)) + " @ " + (str(order.event.start_time)))

                        # Ticket type
                        p.drawString(315, 180, Helper.remove_key(order.ticket.name, "#ENAME"))

                        # Add QRCode
                        p.drawInlineImage('qrcode/qr-' + order_number + '.png', 370, 415, width=140, height=140)

                        # Close the PDF object cleanly, and we're done.
                        p.showPage()
                        p.save()
                        return response
                else:
                    return redirect('index')
            except:
                return redirect('index')
        else:
            return redirect('index')
        # Verify the user is logged in

        # Check the ticket exists
        # Verify that the user who is logged in owns the ticket with this number. If not redirect
        # Take the order_code and use it to generate a qr code
        # Create pdf and draw the details to the page


class EventViewOrders(View):
    template = loader.get_template('orders.html')

    def get(self, request, id, ticket_id):
        # Check if user is logged in
        if request.user.is_authenticated:
            # Check if the user has access
            e = Event.objects.get(id=id)

            if e.event_owner.owner == request.user:
                # Get all of the orders for that event

                # If there is no ticket_id provided then return all orders
                if ticket_id is None:
                    context = {
                        'orders': Order.objects.all().filter(event=e),
                        'event': e
                    }
                else:
                    # Get the ticket object
                    query_ticket = Ticket.objects.get(id=ticket_id)

                    context = {
                        'orders': Order.objects.filter(event=e, ticket=query_ticket),
                        'event': e,
                        'query': True
                    }
                return HttpResponse(self.template.render(context, request))
            else:
                return redirect('index')


class EventViewTickets(View):
    template = loader.get_template('tickets.html')

    def get(self, request, id):
        if request.user.is_authenticated:

            e = Event.objects.get(id=id)

            if e.event_owner.owner == request.user:

                # Get all tickets for this event
                context = {
                    'tickets': Ticket.objects.all().filter(event=e),
                    'event': e
                }
                return HttpResponse(self.template.render(context, request))
            else:
                return redirect('index')
        else:
            return redirect('login')


class ViewOrder(View):
    template = loader.get_template('view-order.html')

    def get(self, request, id):
        # Check that the user is logged in, whether it is the admin or not
        if request.user.is_authenticated:

            # Check if the user is either the event owner or the person who ordered the ticket
            order = Order.objects.get(id=id)

            if order.event.event_owner == request.user or order.user == request.user:

                context = {
                    'order': order
                }

                return HttpResponse(self.template.render(context, request))
            else:
                return redirect('index')
        else:
            return redirect('login')


class ResellTicket(View):
    template = loader.get_template('resell-ticket.html')

    def get(self, request, order_id):
        # Check that the user is logged in,
        if request.user.is_authenticated:
            # Check to make sure the user has access to this ticket
            order = Order.objects.get(id=order_id)

            # Check if the event is over or not
            event_end_time_date = datetime.datetime.combine(order.event.end_date, order.event.end_time)

            if event_end_time_date < datetime.datetime.now():
                messages.warning(request, 'Sorry you cannot resell that ticket because the event is over.')
                return redirect('/my-tickets')
            else:
                if order.user == request.user:

                    context = {
                        'order': order
                    }

                    # Check to see whether or not the ticket can be resold
                    if order.ticket.event.resell == 'Yes':
                        # Now check when the user can resell tickets.

                        # If you can resell anytime
                        if order.ticket.event.resell_when == 'Anytime':
                            # Check to make sure the ticket has not been used

                            if order.used is False:
                                if order.for_sale is False:
                                    return HttpResponse(self.template.render(context, request))
                                else:
                                    messages.warning(request, "Sorry, this ticket is already for sale")
                                    return redirect('index')
                            else:
                                messages.warning(request, "Sorry you cannot resell a ticket that has been used.")
                                return redirect('index')
                        else:
                            # Cannot resell anytime
                            # If the user can sell at sell out
                            if order.ticket.event.resell_when == 'Sell Out':
                                # Now we know that the user can only sell when the event sells out. Check if the event is sold out
                                # Add up all of tickets quantities and all of the tickets sold and figure out if its sold out
                                tickets = Ticket.objects.all().filter(event=order.event)
                                quantity_sold = 0
                                quantity_availible = 0

                                for ticket in tickets:
                                    quantity_sold += ticket.quantity_sold
                                    quantity_availible += ticket.quantity

                                # If sold out then let them
                                if quantity_sold == quantity_availible:
                                    # Check to make sure the ticket isn't used
                                    if order.used is False:
                                        if order.for_sale is False:
                                            return HttpResponse(self.template.render(context, request))
                                        else:
                                            messages.warning(request, "Sorry, this ticket is already for sale")
                                            return redirect('index')
                                    else:
                                        messages.warning(request, "Sorry you cannot resell a ticket that has been used.")
                                        return redirect('index')
                                else:
                                    messages.warning(request, "Sorry, the owner only lets you re-sell when the event is sold out. It is not yet sold out.")
                                    return redirect('index')
                            else:
                                # If it is not Anytime and is not Sell Out then it must be after a certain amount of tickets
                                # Calculate that amount on decide.
                                tickets = Ticket.objects.all().filter(event=order.event)
                                quantity_sold = 0

                                for ticket in tickets:
                                    quantity_sold += ticket.quantity_sold

                                # If the amount of tickets sold is equal or greater than the amount required amount set by the user
                                if quantity_sold >= order.ticket.event.resell_amount:
                                    # Make sure the ticket isn't used.
                                    if order.used is False:
                                        if order.for_sale is False:
                                            return HttpResponse(self.template.render(context, request))
                                        else:
                                            messages.warning(request, "Sorry, this ticket is already for sale")
                                            return redirect('index')
                                    else:
                                        messages.warning(request, "Sorry you cannot resell a ticket that has been used.")
                                        return redirect('index')
                                else:
                                    messages.warning(request, "Sorry you cannot re-sell your ticket yet. The event has to sell more tickets first. Check back soon.")
                                    return redirect('index')
                    else:
                        messages.warning(request, "Sorry, the event owner does not allow you to resell tickets :(")
                        return redirect('index')
                else:
                    return redirect('index')
        else:
            return redirect('login')

    def post(self, request, order_id):
        price = request.POST['price']
        reason = request.POST['reason']
        order = request.POST['order']

        # First make sure the user is still logged in
        if request.user.is_authenticated:

            # Now make sure the user still has access to sell this ticket
            o = Order.objects.get(id=order)

            if o.user == request.user:

                # Now check to make sure the user is charging face value or less

                if Decimal(price) <= o.ticket.price:
                    # Now set the users ticket to used so they cannot use it again
                    o.for_sale = True
                    o.save()

                    # Add ticket to the resell list
                    resell = ResellList(order=o, event=o.event, price=price, reason=reason)
                    resell.save()

                    messages.success(request, "Your ticket has now been put up for sale and will be listed here below.")
                    return redirect('/event/'+str(o.event.id))
                else:
                    messages.warning(request, "Sorry, you cannot charge more than face value for your ticket")
                    return redirect('index')
            else:
                return redirect('index')
        else:
            return redirect('index')


class SellTicket(View):

    def get(self, request):
        messages.success(request, "Please select a ticket you want to resell below")
        return redirect('/my-tickets')


class DiscountCodes(View):
    template = loader.get_template('discount-codes.html')

    def get(self, request, id):
        if request.user.is_authenticated:

            e = Event.objects.get(id=id)

            if e.event_owner.owner == request.user:

                # Get all tickets for this event
                context = {
                    'tickets': Ticket.objects.all().filter(event=e),
                    'event': e,
                    'discount_codes': DiscountCode.objects.all().filter(event=e)
                }
                return HttpResponse(self.template.render(context, request))
            else:
                return redirect('index')
        else:
            return redirect('login')


class EventAddTicket(View):
    template = loader.get_template('add-ticket.html')

    def get(self, request, id):
        if request.user.is_authenticated:

            e = Event.objects.get(id=id)

            if e.event_owner.owner == request.user:

                # Get all tickets for this event
                context = {
                    'tickets': Ticket.objects.all().filter(event=e),
                    'event': e
                }
                return HttpResponse(self.template.render(context, request))
            else:
                return redirect('index')
        else:
            return redirect('login')

    def post(self, request, id):
        if request.user.is_authenticated:

            e = Event.objects.get(id=id)

            if e.event_owner.owner == request.user:

                # Add the ticket
                name = request.POST['name']
                quantity = request.POST['quantity']
                price = request.POST['price']

                new_ticket = Ticket(name=name, quantity=quantity, price=price, event=e)

                try:
                    new_ticket.save()
                    messages.success(request, "Ticket added successfully")
                    return redirect('/manage-event/tickets/'+str(e.id))
                except:
                    messages.warning(request, "Could not add ticket")
                    return redirect('/manage-event/tickets/'+str(e.id))


class EventDeleteTicket(View):

    def get(self, request, id, ticket_id):
        if request.user.is_authenticated:

            e = Event.objects.get(id=id)

            if e.event_owner.owner == request.user:

                ticket = Ticket.objects.get(id=ticket_id)

                ticket.delete()

                messages.success(request, "Ticket successfully deleted")
                return redirect('/manage-event/tickets/'+str(e.id))
            else:
                return redirect('index')
        else:
            return redirect('login')


class DiscountCodesAdd(View):
    template = loader.get_template('add-discount-code.html')

    def get(self, request, id):
        if request.user.is_authenticated:

            e = Event.objects.get(id=id)

            if e.event_owner.owner == request.user:

                # Get all tickets for this event
                context = {
                    'tickets': Ticket.objects.all().filter(event=e),
                    'event': e,
                    'discount_codes': DiscountCode.objects.all().filter(event=e)
                }
                return HttpResponse(self.template.render(context, request))
            else:
                return redirect('index')
        else:
            return redirect('login')

    def post(self, request, id):
        if request.user.is_authenticated:

            e = Event.objects.get(id=id)

            if e.event_owner.owner == request.user:

                code = request.POST['code']
                discount = request.POST['discount']

                discount = DiscountCode(code=code, discount=discount, event=e)

                try:
                    discount.save()
                    messages.success(request, "Discount code added successfully")
                    return redirect('/manage-event/discount-codes/'+str(e.id))
                except:
                    messages.warning(request, "Could not add discount code")
                    return redirect('/manage-event/discount-codes/' + str(e.id))