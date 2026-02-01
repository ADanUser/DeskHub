from django.db import models
from django.conf import settings
from venues.models import Slot

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждена'),
        ('rejected', 'Отклонена'),
        ('canceled', 'Отменена'),
        ('completed', 'Завершена'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings', verbose_name="Пользователь")
    slot = models.OneToOneField(Slot, on_delete=models.CASCADE, related_name='booking', verbose_name="Слот")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"Бронь #{self.id} - {self.user.username}"

