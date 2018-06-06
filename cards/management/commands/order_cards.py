import math
from cards.models import Card, Department
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Update order and page of cards'

    def handle(self, *args, **options):
        departments = Department.objects.all().order_by('id')
        cards_order = 1
        for department in departments:
            cards = Card.objects.filter(fk_department=department, active=True).order_by('id')
            for index, card in enumerate(cards):
                card.page = 1 if index is 0 else int(math.ceil(index / 12))
                card.order = cards_order
                card.save()
                cards_order += 1
        self.stdout.write(self.style.SUCCESS('Successfully updating cards'))
