from django.core import management
from django.core.management.base import BaseCommand
from lvao.tasks import run_clean_csv


class Command(BaseCommand):
    help = "Run clean csv"

    def handle(self, *args, **options):
        run_clean_csv()
