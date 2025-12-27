import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Ожидание PostgreSQL...")

        max_retries = 30
        for i in range(max_retries):
            try:
                conn = connections["default"]
                conn.cursor()
                self.stdout.write(self.style.SUCCESS("База данных доступна!"))
                return
            except OperationalError:
                if i < max_retries - 1:
                    self.stdout.write(f"Попытка {i+1}/{max_retries}...")
                    time.sleep(1)
                else:
                    self.stdout.write(self.style.ERROR("База данных недоступна!"))
                    raise

