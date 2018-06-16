import datetime
import base64
from accounts.models import User
from django.conf import settings
from mail_templated import send_mail
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from cards.functions import new_cards_save


class Command(BaseCommand):
    help = 'Send card packet to all active userses'

    def handle(self, *args, **options):
        list_users = User.objects.filter(is_staff=False, is_superuser=False, is_active=True)

        for user in list_users:
            email = base64.b64encode(bytes(user.email, 'utf-8'))
            email = email.decode("utf-8")

            codes = new_cards_save(5)
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
