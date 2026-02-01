from django.shortcuts import render, redirect, get_object_or_404
from venues.models import Slot
from .models import Booking
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction

def toggle_cart(request, slot_id):
    cart = request.session.get('cart', [])
    slot_id = int(slot_id)
    
    if slot_id in cart:
        cart.remove(slot_id)
        action = 'removed'
        message = "Слот удален из корзины"
    else:
        cart.append(slot_id)
        action = 'added'
        message = "Слот добавлен в корзину"
    
    request.session['cart'] = cart

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'action': action,
            'cart_count': len(cart),
            'message': message
        })

    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))

def cart_remove(request, slot_id):
    return toggle_cart(request, slot_id)

def cart_detail(request):
    cart = request.session.get('cart', [])
    slots = Slot.objects.filter(id__in=cart)
    total_price = sum(slot.price for slot in slots)
    return render(request, 'bookings/cart_detail.html', {'slots': slots, 'total_price': total_price})

@login_required
def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        if not cart:
            messages.warning(request, "Ваша корзина пуста.")
            return redirect('cart_detail')
        
        try:
            with transaction.atomic():
                # Получаем слоты и блокируем их от изменения другими транзакциями
                slots = Slot.objects.filter(id__in=cart).select_for_update()
                
                # Проверяем, что все найденные слоты соответствуют корзине
                # (на случай если какой-то id из корзины не найден в базе)
                found_ids = set(slot.id for slot in slots)
                missing_ids = set(cart) - found_ids
                if missing_ids:
                    # Удаляем несуществующие слоты из корзины
                    cart = [id for id in cart if id not in missing_ids]
                    request.session['cart'] = cart
                    messages.error(request, "Некоторые слоты более не существуют и были удалены из корзины.")
                    return redirect('cart_detail')

                # Проверяем доступность
                unavailable_slots = []
                for slot in slots:
                    if not slot.is_available:
                        unavailable_slots.append(slot)
                
                if unavailable_slots:
                    for slot in unavailable_slots:
                        messages.error(request, f"Слот '{slot}' уже занят. Он был удален из вашей корзины.")
                        if slot.id in cart:
                            cart.remove(slot.id)
                    request.session['cart'] = cart
                    return redirect('cart_detail')
                
                # Создаем бронирования
                for slot in slots:
                    Booking.objects.create(
                        user=request.user,
                        slot=slot,
                        status='pending'
                    )
                    slot.is_available = False
                    slot.save()
                
                # Очищаем корзину
                request.session['cart'] = []
                messages.success(request, "Бронирование успешно оформлено! Ожидайте подтверждения администратором.")
                return redirect('my_bookings')
                
        except Exception as e:
            messages.error(request, f"Произошла ошибка при оформлении: {e}")
            return redirect('cart_detail')

@login_required
def api_bookings_list(request):
    """
    API endpoint that returns a list of user's bookings with their status.
    """
    bookings = Booking.objects.filter(user=request.user).select_related('slot', 'slot__venue').order_by('-created_at')
    data = []
    for booking in bookings:
        data.append({
            'id': booking.id,
            'venue_name': booking.slot.venue.name,
            'date': booking.slot.date,
            'start_time': booking.slot.start_time,
            'end_time': booking.slot.end_time,
            'status': booking.get_status_display(),
            'status_code': booking.status,
            'price': booking.slot.price,
        })
    return JsonResponse({'bookings': data, 'count': len(data)}, json_dumps_params={'ensure_ascii': False, 'indent': 4})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('slot', 'slot__venue').order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        if booking.status in ['pending', 'confirmed']:
            with transaction.atomic():
                booking.status = 'canceled'
                booking.save()
                
                # Освобождаем слот
                booking.slot.is_available = True
                booking.slot.save()
                
                messages.success(request, "Бронирование успешно отменено.")
        else:
             messages.error(request, "Невозможно отменить это бронирование.")
    
    return redirect('my_bookings')
