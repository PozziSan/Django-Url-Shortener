'''
Shortener views
'''
from django.shortcuts import render # We will use it later

from django.http import HttpResponse, Http404, HttpResponseRedirect


# Model
from .models import Shortener

# Custom form

from .forms import ShortenerForm

# Create your views here.


def home_view(request):
    template = 'urlshortener/home.html'

    # template = 'urlshortener/success.html'
    
    context = {}

    # Empty form
    context['form'] = ShortenerForm()

    user_not_authenticated_message = 'User Must Be Authenticated'

    if request.method == 'GET':
        if not request.user.is_authenticated:
            context['errors'] = user_not_authenticated_message

        return render(request, template, context)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            used_form = ShortenerForm(request.POST)

            if used_form.is_valid():

                shortened_object = used_form.save()

                new_url = request.build_absolute_uri('/') + shortened_object.short_url

                long_url = shortened_object.long_url

                context['new_url']  = new_url
                context['long_url'] = long_url

                return render(request, template, context)

            context['errors'] = used_form.errors
        else:
            context['errors'] = user_not_authenticated_message

        return render(request, template, context)


def redirect_url_view(request, shortened_part):

    try:
        shortener = Shortener.objects.get(short_url=shortened_part)

        shortener.times_followed += 1        

        shortener.save()
        
        return HttpResponseRedirect(shortener.long_url)
        
    except:
        raise Http404('Sorry this link is broken :(')