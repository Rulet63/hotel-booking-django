from django.core.management.base import BaseCommand
import time
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    """Django команда для ожидания готовности базы данных"""
    
    help = 'Ждет пока база данных будет готова к подключению'

    def handle(self, *args, **options):
        self.stdout.write('Ожидание базы данных...')
        db_conn = None
        attempts = 0
        
        while not db_conn:
            try:
                # Пытаемся подключиться к базе данных
                db_conn = connections['default']
                db_conn.cursor()
                self.stdout.write(self.style.SUCCESS('База данных доступна!'))
                return
            except OperationalError:
                attempts += 1
                if attempts > 30:  # 30 попыток по 1 секунде = 30 секунд
                    self.stdout.write(self.style.ERROR('База данных не доступна после 30 секунд ожидания'))
                    raise
                self.stdout.write(f'База данных еще не готова, попытка {attempts}/30...')
                time.sleep(1)
