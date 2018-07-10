import datetime
import base64
from events.models import Trivia
from django.conf import settings
from mail_templated import send_mail
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from cards.functions import prize_cards_save


class Command(BaseCommand):
    help = 'Send card packet to all active userses'

    def handle(self, *args, **options):
        trivias = Trivia.objects.all()
        for obj in trivias:
            if not obj.options.filter(is_correct=False).exists():
                user = obj.user
                email = base64.b64encode(bytes(user.email, 'utf-8'))
                email = email.decode("utf-8")

                codes = prize_cards_save()
                site = Site.objects.get_current()
                now = datetime.datetime.now()

                send_mail(
                    'email/send_pack.html',
                    {
                        'name': user.full_name,
                        'codes': codes,
                        'email': email,
                        'site': site,
                        'time': now,
                        'text': 'Este es tu sobre de %s cartas especiales por responder correctamente la Trivia, del día: ' % (len(codes)),
                        'subject': 'Este es tu paquete de cartas especiales (Trivia)'
                    },
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email]
                )
        self.stdout.write(self.style.SUCCESS('Successfully send emails'))
