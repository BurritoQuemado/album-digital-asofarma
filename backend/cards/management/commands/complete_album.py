from cards.functions import code_save
from cards.models import Card, Code
from django.core.management.base import BaseCommand, CommandError
from accounts.models import User


class Command(BaseCommand):
    help = "Fill the album for a specified user"

    def add_arguments(self, parser):
        parser.add_argument("user_email", nargs="+", type=str)

    def handle(self, *args, **options):
        for user_email in options["user_email"]:
            try:
                user = User.objects.get(
                    email=user_email, is_active=True, is_superuser=False, is_staff=False
                )
            except User.DoesNotExist:
                raise CommandError('User "%s" does not exist' % user_email)

            cards = Card.objects.all()
            for card in cards:
                if not Code.objects.filter(fk_card=card, fk_user=user).exists():
                    code = code_save()
                    c = Code(code=code, fk_card=card, fk_user=user)
                    c.save()
            self.stdout.write(
                self.style.SUCCESS("All cards added to user %s" % (user_email))
            )
