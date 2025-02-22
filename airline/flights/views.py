from django.shortcuts import render
from .models import flight, airport
from django.http import JsonResponse, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'flights/index.html')

def airports(request, id):
    d = airport.objects.get(pk=id)
    return HttpResponse(f"Airport {id}")

def flights(request, id):
    d = flight.objects.get(pk=id)
    return HttpResponse(f"Flight {id}")

def search(request):
    if request.GET.get('type') == "flights":
        json = {
            "flights":[]
        }
        data = flight.objects.filter(origin__country__contains=request.GET.get('origin','').upper(),
                                     destination__country__contains=request.GET.get('destination','').upper())
        for d in data:
            attributes = {
                "id":d.pk,
                "origin_country":d.origin.country,
                "origin_city":d.origin.country,
                "origin_id":d.origin.pk,
                "destination_country":d.destination.country,
                "destination_city":d.destination.city,
                "destination_id":d.destination.pk,
                "duration":d.duration
            }
            json["flights"].append(attributes)
        
        return JsonResponse(json)
    elif request.GET.get('type') == "airports":
        json = {
            "airports":[]
        }
        data = airport.objects.filter(country__contains=request.GET.get('country','').upper(),
                                      city__contains=request.GET.get('city','').upper())
        for d in data:
            attributes = {
                "id":d.pk,
                "country":d.country,
                "city":d.city,
                "name":d.name,
                "map":f"{d.lat_decimal},{d.lon_decimal}"
            }
            json["airports"].append(attributes)
        
        return JsonResponse(json)