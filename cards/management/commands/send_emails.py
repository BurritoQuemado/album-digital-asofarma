import string
import random
import datetime
import numpy as np
import base64
from cards.models import Card, Code, Rarity
from accounts.models import User
from django.conf import settings
from mail_templated import send_mail
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


def get_cards():
    # opening connection with the database
    packet = []
    packet_card = []
    total_cards = 5
    # number of the cards in the packet
    for card_number in range(1, total_cards + 1):
        # We get de rarity of the card and after we will choose a card in that category
        # if we wish change the probability we need change the values in the p
        rarity = np.random.choice(4, p=[settings.PROBABILITY_SPECIAL, settings.PROBABILITY_LOW, settings.PROBABILITY_MEDIUM, settings.PROBABILITY_HIGH])
        rarity = rarity + 1

        rarity_id = Rarity.objects.get(id=rarity)
        cards = Card.objects.filter(fk_rarity=rarity_id, active=True, wave=1).values('id')
        # we choose all the cards with the rarity selected
        for card in cards:
            packet_card.append(card['id'])

        # we choose one card and finally, put the card in the packet
        packet.append(np.random.choice(packet_card))

    return packet


def id_generator(size=8, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def code_save():
    """ A function to generate a 8 character code and see if it has been used and contains naughty words."""
    code = id_generator()  # create one
    code_is_wrong = True
    while code_is_wrong:  # keep checking until we have a valid code
        code_is_wrong = False
        other_objs_with_code = Code.objects.filter(code=code)
        if len(other_objs_with_code) > 0:
            # if any other objects have current code
            code_is_wrong = True
        if code_is_wrong:
            # create another code and check it again
            code = id_generator()
    return code


def new_cards_save():
    packet_codes = []

    for card in get_cards():
        # we generate the code of the card
        code = code_save()
        packet_codes.append(code)
        # we save the packet of cards
        c = Code(code=code, fk_card=Card.objects.get(id=card), )
        c.save()
    # return the packet of cards
    return packet_codes


def random_string(length):
    """
    :param length: Size of the card string
    :return: Random string
    """
    return ''.join(random.choice(string.ascii_letters) for m in range(length))


class Command(BaseCommand):
    help = 'Send card packet to all active userses'

    def handle(self, *args, **options):
        list_users = User.objects.filter(is_staff=False, is_superuser=False, is_active=True)

        for user in list_users:
            email = base64.b64encode(bytes(user.email, 'utf-8'))
            email = email.decode("utf-8")

            codes = new_cards_save()
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
