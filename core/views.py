from django.shortcuts import render
from core.models import EVChargingLocation

# Create your views here.
def index(request):
    stations = list(EVChargingLocation.objects.values('latitude', 'longitude')[:100])

    context = {
        'stations': stations,
    }
    return render(request, 'index.html', context)