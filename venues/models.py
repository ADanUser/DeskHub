from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Город")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название коворкинга")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='venues', verbose_name="Город")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='venues/', blank=True, null=True, verbose_name="Фото")
    
    class Meta:
        verbose_name = "Коворкинг"
        verbose_name_plural = "Коворкинги"

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class Slot(models.Model):
    RESOURCE_TYPES = (
        ('workplace', 'Рабочее место'),
        ('meeting_room', 'Переговорная комната'),
    )

    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='slots', verbose_name="Коворкинг")
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default='workplace', verbose_name="Тип ресурса")
    date = models.DateField(verbose_name="Дата")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_available = models.BooleanField(default=True, verbose_name="Доступен")

    class Meta:
        verbose_name = "Слот"
        verbose_name_plural = "Слоты"
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.venue.name} - {self.get_resource_type_display()} ({self.date} {self.start_time})"

