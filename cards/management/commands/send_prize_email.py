import datetime
import base64
from django.conf import settings
from mail_templated import send_mail
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from cards.functions import prize_cards_save
from events.models import Prediction


class Command(BaseCommand):
    help = 'Send card packet to all active userses'

    def handle(self, *args, **options):
        predictions = Prediction.objects.filter(user__is_staff=False, user__is_superuser=False, user__is_active=True)
        for prediction in predictions:
            if prediction.away_result is prediction.match.away_result and prediction.home_result is prediction.match.home_result:
                user = prediction.user
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
                        'time': now
                    },
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email]
                )
        self.stdout.write(self.style.SUCCESS('Successfully send emails'))
