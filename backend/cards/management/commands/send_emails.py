import datetime
import base64
from accounts.models import User
from django.conf import settings
from templated_email import send_templated_mail
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

            send_templated_mail(
                template_name='send_pack',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                context={
                    'name': user.full_name,
                    'codes': codes,
                    'email': email,
                    'site': site,
                    'time': now,
                    'text': 'Este es tu sobre de %s cartas del día: ' % (len(codes)),
                    'subject': 'Este es tu paquete de cartas'
                },
                # cc=['cc@example.com'],
                # bcc=['bcc@example.com'],
                # headers={'My-Custom-Header':'Custom Value'},
                template_prefix="email/",
                template_suffix="html",
            )
        self.stdout.write(self.style.SUCCESS('Successfully send emails'))
