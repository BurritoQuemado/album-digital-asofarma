import string
import random
import datetime
import base64
import numpy as np
# from mail_templated import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from .forms import EmailSaveForm
from accounts.models import User
from .models import Card, Code, Rarity, Department
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.template import Context


class EmailSaveView(UpdateView):
    model = Code
    form_class = EmailSaveForm
    template_name = 'cards/card_save_email.html'
    success_url = '/'  # reverse_lazy('card')
    success_message = 'Se ha guardado la carta a tu álbum'

    def get_object(self, queryset=None):
        obj = Code.objects.get(code=self.kwargs['code'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = Code.objects.get(code=self.kwargs['code'])
        context['card'] = code.fk_card
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        email = base64.b64decode(self.kwargs['email'])
        email = email.decode("utf-8")
        user = User.objects.get(email=email)

        # the users redeem the codes or change the codes
        self.object.fk_user = user
        self.object.save()
        return super().form_valid(form)


class CardList(ListView):
    template_name = 'cards/cards_list.html'
    model = Card
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department'] = Department.objects.get(slug=self.kwargs['slug'])
        context['badge'] = Card.objects.get(fk_department__slug=self.kwargs['slug'], is_badge=True)
        return context

    def get_queryset(self, *args, **kwargs):
        cards = Card.objects.filter(fk_department__slug=self.kwargs['slug'], is_badge=False).order_by('id')
        return cards


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
        cards = Card.objects.filter(fk_rarity=rarity_id, active=True).values('id')
        # we choose all the cards with the rarity selected
        for card in cards:
            packet_card.append(card['id'])

        # we choose one card and finally, put the card in the packet
        packet.append(np.random.choice(packet_card))

    return packet


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
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


def send_cards(request):
    # we expect the target, and department in case the target be users we send
    # the email to all the users if not we select the target with the info send in the other parameters

    list_users = User.objects.filter(is_staff=False, is_superuser=False, is_active=True)

    for user in list_users:
        email = base64.b64encode(bytes(user.email, 'utf-8'))
        email = email.decode("utf-8")

        codes = new_cards_save()
        site = get_current_site(request)
        now = datetime.datetime.now()

        # send_mail(
        #     'email/send_pack.html',
        #     {
        #         'name': user.full_name,
        #         'codes': codes,
        #         'email': email,
        #         'site': site,
        #         'time': now
        #     },
        #     settings.DEFAULT_FROM_EMAIL,
        #     [user.email]
        # )

        plaintext = get_template('email/send_pack.txt')
        htmly = get_template('email/send_pack.html')

        ctx = {
            'name': user.full_name,
            'codes': codes,
            'email': email,
            'site': site,
            'time': now
        }

        message = render_to_string('email/send_pack.html', ctx)

        text_content = plaintext.render(d)
        html_content = htmly.render(d)

        msg = EmailMultiAlternatives(
            'Este es tu paquete de cartas: ',
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

    data = {'success': 'OK'}
    return JsonResponse(data)


def users_cards_save_email(request, code, user):
    # we decode the string in base64 and we search with the code and with email and we try to redeem the code
    try:
        email = base64.b64decode(user)
        email = email.decode("utf-8")
        user = User.objects.get(email=email)

        # the users redeem the codes or change the codes
        update_code = Code.objects.get(code=code)
        update_code.fk_user = user
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
