from django.http import JsonResponse
from django.shortcuts import render
from core.models import EVChargingLocation
from geopy.distance import geodesic

# Create your views here.
def index(request):
    stations = list(EVChargingLocation.objects.values('latitude', 'longitude')[:100])

    context = {
        'stations': stations,
    }
    return render(request, 'index.html', context)


def nearest_station(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    user_location = (latitude, longitude)
    station_distances = {}

    for station in EVChargingLocation.objects.all()[:100]:
        station_location = (station.latitude, station.longitude)

        # calculate distance

        distance = geodesic(user_location, station_location).km
        station_distances[distance] = station_location

    min_distance = min(station_distances)
    station_coords = station_distances[min_distance]

    return JsonResponse({
        'coordinates': station_coords,
        'distance': min_distance,
    })