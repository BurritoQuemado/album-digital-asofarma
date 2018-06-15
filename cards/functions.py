import string
import numpy as np
import random
from cards.models import Card, Code, Rarity
from django.conf import settings


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
