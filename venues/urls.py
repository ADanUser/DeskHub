from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('search/', views.search, name='venue_search'),
    path('api/venues/', views.api_venues_list, name='api_venues_list'),
    path('api/venues/<int:venue_id>/', views.api_venue_detail, name='api_venue_detail'),
    path('<int:venue_id>/', views.venue_detail, name='venue_detail'),
]