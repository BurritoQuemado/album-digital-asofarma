from django.http import HttpResponse
import numpy as np
from .models import Card, Code, Rarity, Department
from django.views.generic.list import ListView
import string
import random
from django.core.mail import send_mail
from accounts.models import User
import base64
import environ
from django.http import JsonResponse

root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, True), ALLOWED_HOSTS=(list, []),)  # set default values and casting
environ.Env.read_env(root('.env'))  # reading .env file


class CardList(ListView):
    template_name = 'cards/cards_list.html'
    model = Card
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department'] = Department.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self, *args, **kwargs):
        return Card.objects.filter(fk_department__slug=self.kwargs['slug']).order_by('description')


def get_cards():
    # opening connection with the database
    packet = []
    packet_card = []
    total_cards = 7
    # number of the cards in the packet
    for card_number in range(1, total_cards + 1):
        # We get de rarity of the card and after we will choose a card in that category
        # if we wish change the probability we need change the values in the p
        rarity = np.random.choice(3, p=[env('PROBABILITY_LOW'), env('PROBABILITY_MEDIUM'), env('PROBABILITY_HIGH')])
        rarity = rarity + 1

        rarity_id = Rarity.objects.get(id=rarity)
        cards = Card.objects.filter(fk_rarity=rarity_id, active=True).values('id')
        # we choose all the cards with the rarity selected
        for card in cards:
            packet_card.append(card['id'])

        # we choose one card and finally, put the card in the packet
        packet.append(np.random.choice(packet_card))

    return packet


def new_cards_save():
    packet_codes = []

    for card in get_cards():
        # we generate the code of the card
        code = random_string(20)
        packet_codes.append(code)
        # we save the packet of cards
        c = Code(code=code, fk_card=Card.objects.get(id=card), )
        c.save()
    # return the packet of cards
    return packet_codes


def send_cards(request, target, department=0):
    # we expect the target, and department in case the target be users we send
    # the email to all the users if not we select the target with the info send in the other parameters
    subject = 'Envio de cartas'
    from_email = 'jason@gnuin0.com'
    message = 'This is my test message'
    server = request.META['HTTP_HOST']

    if target == 'users':
        # send the email to all the users
        list_users = User.objects.filter(is_staff=False, is_superuser=False, is_active=True).values_list('email')
    else:
        return HttpResponse('The option its incorrect')

    for user_email in list_users:
        email = base64.b64encode(bytes(user_email[0], 'utf-8'))
        email = email.decode("utf-8")
        html_message = []

        for codes in new_cards_save():

            # encode email to base64
            html_message.append('<p><a href=http://'+server+'/cards/redeem/'+codes+'/'+email+'/>Click para redimir</a></p>')

        # we send the email with the codes of cards ready for redeem
        html_message = ''.join(map(str, html_message))
        send_mail(subject, message, from_email, user_email, fail_silently=False, html_message=html_message)

    data = {'success': 'OK'}
    return JsonResponse(data)


def users_cards_save_email(request, code, user):
    # we decode the string in base64 and we search with the code and with email and we try to redeem the code
    try:
        email = base64.b64decode(user)
        email = email.decode("utf-8")
        user = list(User.objects.filter(email=email).values_list('id'))

        # the users redeem the codes or change the codes
        update_code = Code.objects.get(code=code)
        update_code.fk_user = User.objects.get(id=user[0][0])
        update_code.save()

        data = {'success': 'OK'}
        return JsonResponse(data)
    except Exception as e:
        data = {'success': "FAIL"}
        return JsonResponse(data)


def users_cards_save_session(request, code, user):
    # we decode the string in base64 and we search with the code and with email and we try to redeem the code
    try:
        if request.user.id > 1:
            # the users redeem the codes or change the codes
            update_code = Code.objects.get(code=code)
            update_code.fk_user = User.objects.get(id=request.user.id)
            update_code.save()

            data = {'success': 'OK'}
            return JsonResponse(data)

        data = {'success': "FAIL"}
        return JsonResponse(data)
    except Exception as e:
        data = {'success': "FAIL"}
        return JsonResponse(data)


def random_string(length):
    """
    :param length: Size of the card string
    :return: Random string
    """
    return ''.join(random.choice(string.ascii_letters) for m in range(length))
