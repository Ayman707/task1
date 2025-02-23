from django.shortcuts import render
from .models import flight, airport, passenger
from django.http import JsonResponse, Http404

# Create your views here.
def index(request):
    return render(request, 'flights/index.html')

def airports(request, id):
    if(id < 1 or id >9300):
        raise Http404("no airport")
    d = airport.objects.get(pk=id)
    if d.name == "N/A":
        name = f"{d.country.capitalize()} airport"
    else:
        name = d.name

    depdata = []
    deps = d.departures.all()
    r = 1
    for dep in deps:
        depdata.append(
            {
                "r": r,
                "num": dep.pk,
                "destination": dep.destination
            }
        )
        r += 1

    arrdata = []
    arrs = d.arrivals.all()
    r = 1
    for arr in arrs:
        arrdata.append(
            {
                "r": r,
                "num": arr.pk,
                "origin":arr.origin
            }
        )
        r += 1

    return render(request, "flights/airport.html", {
        "country":d.country,
        "city":d.city,
        "name":name,
        "iata":d.iata_code,
        "icao":d.icao_code,
        "location":f"https://www.google.com/maps/place/{d.lat_decimal},{d.lon_decimal}",
        "departures": depdata,
        "arrivals":arrdata
    })

def flights(request, id):
    
    if request.method == "POST":
        f = request.POST.get('first')
        l = request.POST.get('last')
        if f != "" and l != "":
            if len(passenger.objects.filter(first=f.capitalize(), last=l.capitalize())) == 0:
                p = passenger(first=f.capitalize(), last=l.capitalize())
                p.save()
                flight.objects.get(pk=id).passengers.add(p)
            else:
                p = passenger.objects.get(first=f.capitalize(), last=l.capitalize())
                flight.objects.get(pk=id).passengers.add(p)


    if(id < 1 or id > flight.objects.all().count()):
        raise Http404("no airport")
    
    d = flight.objects.get(pk=id)

    passengerdata = []
    r = 1
    for p in d.passengers.all():
        row = {
            "r":r,
            "first":p.first,
            "last":p.last
        }
        passengerdata.append(row)
        r += 1

    return render(request, "flights/flight.html", {
        "id":id,
        "origin":d.origin,
        "destination":d.destination,
        "duration":d.duration,
        "passenger":passengerdata
    })

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
                "origin_city":d.origin.city,
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