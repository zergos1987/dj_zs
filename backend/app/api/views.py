from django.shortcuts import render
from django.http import HttpResponse



# Create your views here.

def index(request):
    return HttpResponse(200)

    if request.user.is_authenticated():
        user_settings = app_settings.objects.filter(user=request.user).first()
    else:
        user_settings = app_settings.objects.filter(user__isnull=True).first()

    context = {
		'app_settings': user_settings,
        'data': {'col': 'test'},
	}
    template = 'api/index.html'

    return render(request, template, context)