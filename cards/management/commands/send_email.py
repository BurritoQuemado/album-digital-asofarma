import datetime
import base64
from django.core.management.base import BaseCommand, CommandError
from accounts.models import User
from django.conf import settings
from mail_templated import send_mail
from django.contrib.sites.models import Site
from cards.functions import new_cards_save


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('user_email', nargs='+', type=str)

    def handle(self, *args, **options):
        for user_email in options['user_email']:
            try:
                user = User.objects.get(email=user_email, is_active=True, is_superuser=False, is_staff=False)
            except User.DoesNotExist:
                raise CommandError('User "%s" does not exist' % user_email)

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
                    'time': now,
                    'text': 'Este es tu sobre de %s cartas del día: ' % (len(codes)),
                    'subject': 'Este es tu paquete de cartas especiales'
                },
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )

            self.stdout.write(self.style.SUCCESS('Send email to "%s"' % user_email))
