import time

from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


@cache_page(60 * 15)
@vary_on_cookie
def HomePage(request):
    time.sleep(3)
    return HttpResponse("Home Page Test")
