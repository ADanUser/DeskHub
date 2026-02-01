from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import City, Venue, Slot

def index(request):
    cities = City.objects.all()
    return render(request, 'venues/index.html', {'cities': cities})

def search(request):
    city_id = request.GET.get('city')
    date_str = request.GET.get('date')
    resource_type = request.GET.get('resource_type')
    
    # Оптимизация: сразу подгружаем связанные города, чтобы избежать N+1 запросов в шаблоне
    venues = Venue.objects.select_related('city').all()
    
    if city_id:
        venues = venues.filter(city_id=city_id)
    
    if date_str or resource_type:
        slot_filter = {'is_available': True}
        if date_str:
            slot_filter['date'] = date_str
        if resource_type:
            slot_filter['resource_type'] = resource_type
    
        filter_kwargs = {f'slots__{k}': v for k, v in slot_filter.items()}
        venues = venues.filter(**filter_kwargs).distinct()
    
    paginator = Paginator(venues, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    context = {
        'venues': page_obj,
        'cities': City.objects.all(),
        'selected_city': int(city_id) if city_id else '',
        'selected_date': date_str,
        'selected_type': resource_type,
    }
    return render(request, 'venues/search_results.html', context)

def venue_detail(request, venue_id):
    # Оптимизация: сразу подгружаем город
    venue = get_object_or_404(Venue.objects.select_related('city'), pk=venue_id)
    
    date_str = request.GET.get('date')
    resource_type = request.GET.get('resource_type')
    
    slots = Slot.objects.filter(venue=venue, is_available=True)
    
    if date_str:
        slots = slots.filter(date=date_str)
    
    if resource_type:
        slots = slots.filter(resource_type=resource_type)
        
    slots = slots.order_by('date', 'start_time')
    
    paginator = Paginator(slots, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'venue': venue,
        'slots': page_obj,
        'selected_date': date_str,
        'selected_type': resource_type,
    }
    return render(request, 'venues/venue_detail.html', context)

def api_venues_list(request):
    """
    API endpoint that returns a list of venues.
    """
    venues = Venue.objects.select_related('city').all()
    data = []
    for venue in venues:
        data.append({
            'id': venue.id,
            'name': venue.name,
            'city': venue.city.name,
            'address': venue.address,
            'description': venue.description,
            'image_url': venue.image.url if venue.image else None,
        })
    return JsonResponse({'venues': data, 'count': len(data)}, json_dumps_params={'ensure_ascii': False, 'indent': 4})

def api_venue_detail(request, venue_id):
    """
    API endpoint that returns venue details and available slots.
    """
    venue = get_object_or_404(Venue.objects.select_related('city'), pk=venue_id)
    slots = Slot.objects.filter(venue=venue, is_available=True).order_by('date', 'start_time')
    
    slots_data = []
    for slot in slots:
        slots_data.append({
            'id': slot.id,
            'date': slot.date,
            'start_time': slot.start_time,
            'end_time': slot.end_time,
            'resource_type': slot.get_resource_type_display(),
            'resource_type_code': slot.resource_type,
            'price': slot.price,
        })
        
    data = {
        'id': venue.id,
        'name': venue.name,
        'city': venue.city.name,
        'address': venue.address,
        'description': venue.description,
        'image_url': venue.image.url if venue.image else None,
        'slots': slots_data,
        'slots_count': len(slots_data)
    }
    
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})

