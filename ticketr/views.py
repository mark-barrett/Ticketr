from django.http import HttpResponse
from django.template import loader

from .models import *


def index(request):
    # Get the index.html template in the templates folder
    template = loader.get_template('index.html')
    context = {

    }
    # Return the template as a HttpResponse
    return HttpResponse(template.render(context, request))


def event(request):
    # Get the index.html template in the templates folder
    template = loader.get_template('event.html')
    context = {

    }
    # Return the template as a HttpResponse
    return HttpResponse(template.render(context, request))
