from django.shortcuts import render
from django.http import HttpResponse

from spa.models import app_settings

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        user_settings = app_settings.objects.filter(user=request.user).first()
    else:
        user_settings = app_settings.objects.filter(user__isnull=True).first()

    context = {
		'app_settings': user_settings.json_data,
        'data': {'col': 'test'},
	}
    template = 'spa/index.html'

    return render(request, template, context)