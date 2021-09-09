import os
import xml.etree.ElementTree as ET
from django.contrib.gis.measure import Distance, D
from django.contrib.gis.geos import fromstr
from rest_framework.decorators import api_view
from .models import Places
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import manager, query
from django.shortcuts import render
from.serializers import PlaceSerializer
# Create your views here.


class AllPlaces(APIView):
    def get(self, request, format=None):
        places = Places.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)


class getKmlData(APIView):
    def get(self, request, format=None):
        kml = open(
            '/home/hugur/deneme1.kml').read()

        return Response(kml)


@api_view(['GET'])
def getTypes(request):
    types = Places.objects.filter().values('type').distinct()
    return Response(types)

@api_view(['POST'])
def writeKml(request):
    name = request.data['name']
    type = request.data['type']
    latlng = request.data['latlng']
    split = latlng.split(", ")
    lnglat = split[1] + ", " + split[0]
    writing(name, type, lnglat)
    return Response("success")


@api_view(['POST'])
def getPlaces(request):
    radius = request.data['radius']/1000
    lat = request.data['latlng']['lat']
    lng = request.data['latlng']['lng']
    pnt = fromstr('POINT(%s %s)' % (lng, lat), srid=4326)

    if(request.data['type'] != ""):
        places = Places.objects.filter(point__distance_lt=(
            pnt, D(km=radius)), type=request.data['type'])
    else:
        places = Places.objects.filter(point__distance_lt=(pnt, D(km=radius)))

    serializer = PlaceSerializer(places, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def addDB(request):
    kml = ET.parse('/home/hugur/deneme.kml')

    for placemark in kml.iter('Placemark'):

        nameKML = placemark.find('name').text
        typeKML = placemark.find('description').text
        lnglat = placemark.find('Point').find("coordinates").text
        split = lnglat.split(", ")
        pnt = fromstr('POINT(%s %s)' % (split[0], split[1]), srid=4326)
        if Places.objects.filter(name=nameKML).exists():
            print("exist")
        else:
            item = Places(name=nameKML, type=typeKML, point=pnt)
            item.save()

    return Response("success")

@api_view(['POST'])
def deletePlaces(request):
    name = request.data['deletedName']
    Places.objects.get(name=name).delete()

    return Response("success")

# KML'ye yaz
def writing(isim, tip, latlng):
    import xml.etree.ElementTree as ET
    if os.path.exists("/home/hugur/deneme.kml"):

        tree = ET.parse("/home/hugur/deneme.kml")
        root = tree.getroot()
    else:
        root = ET.Element("folder")

    placemark = ET.Element("Placemark")
    root.append(placemark)
    name = ET.SubElement(placemark, 'name')
    name.text = isim
    type = ET.SubElement(placemark, 'description')
    type.text = tip
    point = ET.SubElement(placemark, 'Point')
    coordinates = ET.SubElement(point, 'coordinates')
    coordinates.text = latlng

    with open('/home/hugur/deneme.kml', 'a'):
        ET.ElementTree(root).write('/home/hugur/deneme.kml')
