from django.core.management.base import BaseCommand
from venues.models import City, Venue, Slot
from django.utils import timezone
import datetime
import random
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates the database with large dataset for performance testing (100+ venues, 10k+ slots)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing old data...')
        Slot.objects.all().delete()
        Venue.objects.all().delete()
        City.objects.all().delete()

        cities_names = [
            'Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань',
            'Челябинск', 'Тюмень', 'Самара', 'Владивосток', 'Красноярск',
            'Краснодар', 'Уфа', 'Сочи', 'Грозный', 'Махачкала', 
            'Хабаровск', 'Мурманск'
        ]
        
        prefixes = ['Бизнес', 'Смарт', 'Техно', 'Арт', 'Инно', 'Эко', 'Про', 'Сити', 'Мега', 'Опен', 'Старт', 'Фьюжн']
        suffixes = ['Спейс', 'Хаб', 'Лофт', 'Офис', 'Зона', 'Плейс', 'Лаб', 'Ворк', 'Рум', 'Центр', 'Поинт', 'Холл']
        streets = ['Ленина', 'Мира', 'Советская', 'Гагарина', 'Пушкина', 'Кирова', 'Садовая', 'Победы', 'Маркса', 'Калинина']

        self.stdout.write('Generating data...')
        
        today = timezone.now().date()
        total_venues = 0
        total_slots = 0

        for city_name in cities_names:

            slug = slugify(city_name, allow_unicode=True) 
            if not slug: 
                 slug = f"city-{random.randint(1000, 9999)}"

            city = City.objects.create(name=city_name, slug=slug)

            for i in range(6):
                name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
                if Venue.objects.filter(name=name).exists():
                    name = f"{name} {city_name}"
                
                address = f"ул. {random.choice(streets)}, д. {random.randint(1, 200)}"
                
                venue = Venue.objects.create(
                    name=name,
                    city=city,
                    address=address,
                    description=f'Уютное пространство "{name}" в городе {city_name}. Высокоскоростной интернет, чай/кофе.',
                    image='venues/office.jpg'
                )
                total_venues += 1

                slots_batch = []
                for day_offset in range(30):
                    current_date = today + datetime.timedelta(days=day_offset)

                    slots_batch.append(Slot(
                        venue=venue,
                        resource_type='workplace',
                        date=current_date,
                        start_time=datetime.time(9, 0),
                        end_time=datetime.time(13, 0),
                        price=500.00
                    ))
                    slots_batch.append(Slot(
                        venue=venue,
                        resource_type='workplace',
                        date=current_date,
                        start_time=datetime.time(14, 0),
                        end_time=datetime.time(18, 0),
                        price=600.00
                    ))
                    slots_batch.append(Slot(
                        venue=venue,
                        resource_type='meeting_room',
                        date=current_date,
                        start_time=datetime.time(10, 0),
                        end_time=datetime.time(12, 0),
                        price=1500.00
                    ))
                    slots_batch.append(Slot(
                        venue=venue,
                        resource_type='meeting_room',
                        date=current_date,
                        start_time=datetime.time(14, 0),
                        end_time=datetime.time(16, 0),
                        price=1500.00
                    ))
                
                Slot.objects.bulk_create(slots_batch)
                total_slots += len(slots_batch)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total_venues} venues and {total_slots} slots in {len(cities_names)} cities!'))