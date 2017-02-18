from django.http import HttpResponse
from django.template import loader

from .models import *


def index(request):
    # Get the index.html template in the templates folder
    template = loader.get_template('index.html')
    context = {
        ## We want all categories objects to be sent ##
        'categories': Category.objects.all(),
    }
    # Return the template as a HttpResponse
    return HttpResponse(template.render(context, request))


def event(request, id):
    # Get the index.html template in the templates folder
    template = loader.get_template('event.html')
    context = {
        ## Get the event with the id passed as a parameter ##
        'event' : Event.objects.get(id=id)
    }
    # Return the template as a HttpResponse
    return HttpResponse(template.render(context, request))
