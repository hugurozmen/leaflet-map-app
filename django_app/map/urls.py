from django.urls import path, include
from map import views

urlpatterns = [
    path('all-places', views.AllPlaces.as_view()),
    path('get-places', views.getPlaces),
    path('get-kml', views.getKmlData.as_view()),
    path('write-kml',views.writeKml),
    path('add-db', views.addDB),
    path('delete-place', views.deletePlaces),
    path('get-types', views.getTypes),
    

]
