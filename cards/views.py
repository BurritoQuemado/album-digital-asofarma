import base64
import math
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from .forms import EmailSaveForm, AddCodeForm, SendCodeForm
from accounts.models import User
from .models import Card, Code, Department
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, FormView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

decorators = [login_required]


@method_decorator(decorators, name='dispatch')
class EmailSaveView(SuccessMessageMixin, UpdateView):
    model = Code
    form_class = EmailSaveForm
    template_name = 'cards/card_save_email.html'
    success_message = 'Se ha guardado la carta a tu álbum'

    def get_success_url(self, **kwargs):
        code = Code.objects.get(code=self.kwargs['code'])
        cards = Card.objects.filter(fk_department__slug=code.fk_card.fk_department.slug, active=True).order_by('id')
        page = 0
        if cards.count() > 12:
            for index, card in enumerate(cards):
                if code.fk_card.id is card.id:
                    page = index
        if page > 0:
            return reverse('cards:card_list', kwargs={'pk': self.request.user.id, 'slug': code.fk_card.fk_department.slug}) + '?page=' + str(int(math.ceil(page / 12))) + '#' + str(code.fk_card.id)
        else:
            return reverse('cards:card_list', kwargs={'pk': self.request.user.id, 'slug': code.fk_card.fk_department.slug}) + '#' + str(code.fk_card.id)

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

        self.object.fk_user = user
        self.object.save()
        return super().form_valid(form)


@method_decorator(decorators, name='dispatch')
class SendCodeView(SuccessMessageMixin, UpdateView):
    model = Code
    template_name = 'cards/card_send_code.html'
    form_class = SendCodeForm
    success_message = "Se ha enviado la carta con éxito"

    def get_success_url(self, **kwargs):
        return reverse('cards:card_cover', kwargs={'pk': self.request.user.id})

    def get_object(self, queryset=None):
        obj = get_object_or_404(Code, code=self.kwargs['code'], fk_user=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = Code.objects.get(code=self.kwargs['code'])
        context['card'] = code.fk_card
        return context

    def get_form_kwargs(self):
        kwargs = super(SendCodeView, self).get_form_kwargs()
        kwargs.update({'current_user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = form.cleaned_data['user']
        self.object.fk_user = user
        self.object.save()
        return super().form_valid(form)


@method_decorator(decorators, name='dispatch')
class AddCodeView(SuccessMessageMixin, FormView):
    template_name = 'cards/card_save_form.html'
    form_class = AddCodeForm
    success_message = "Se ha guardado la carta en tu álbum"

    def get_success_url(self, **kwargs):
        code = Code.objects.get(code=self.form.cleaned_data['code'])
        cards = Card.objects.filter(fk_department__slug=code.fk_card.fk_department.slug, active=True).order_by('id')
        page = 0
        if cards.count() > 12:
            for index, card in enumerate(cards):
                if code.fk_card.id is card.id:
                    page = index
        if page > 0:
            return reverse('cards:card_list', kwargs={'pk': self.request.user.id, 'slug': code.fk_card.fk_department.slug}) + '?page=' + str(int(math.ceil(page / 12))) + '#' + str(code.fk_card.id)
        else:
            return reverse('cards:card_list', kwargs={'pk': self.request.user.id, 'slug': code.fk_card.fk_department.slug}) + '#' + str(code.fk_card.id)

    def form_valid(self, form):
        self.form = form
        user = self.request.user
        code = Code.objects.get(code=form.cleaned_data['code'])
        code.fk_user = user
        code.save()
        return super().form_valid(form)


class CoverView(DetailView):
    model = User
    template_name = 'cards/card_cover.html'
    context_object_name = 'user_object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cards = Card.objects.filter(active=True).order_by('id')
        codes = Code.objects.filter(fk_user_id=self.kwargs['pk']).values('fk_card').distinct()
        context['codes'] = codes.count()
        context['total'] = cards.count()
        context['album_user'] = User.objects.get(pk=self.kwargs['pk'])
        departments = Department.objects.all().order_by('id')
        for department in departments:
            department_codes = Code.objects.filter(fk_user_id=self.kwargs['pk'], fk_card__fk_department=department)
            if department_codes.exists():
                department.codes = department_codes.count()
            else:
                department.codes = 0
            department.cards = Card.objects.filter(fk_department=department, active=True).count()
        context['departments'] = departments
        return context


class CardList(ListView):
    template_name = 'cards/cards_list.html'
    model = Card
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        badge = Card.objects.get(fk_department__slug=self.kwargs['slug'], is_badge=True, active=True)
        badge_codes = Code.objects.filter(fk_user_id=self.kwargs['pk'], fk_card=badge)
        if badge_codes.exists():
            badge.obtained = True
            badge.codes = badge_codes
        departments = Department.objects.all().order_by('id')
        for department in departments:
            department_codes = Code.objects.filter(fk_user_id=self.kwargs['pk'], fk_card__fk_department=department)
            if department_codes.exists():
                department.codes = department_codes.count()
            else:
                department.codes = 0
            department.cards = Card.objects.filter(fk_department=department, active=True).count()
        context['department'] = Department.objects.get(slug=self.kwargs['slug'])
        context['departments'] = departments
        context['badge'] = badge
        context['album_user'] = User.objects.get(pk=self.kwargs['pk'])
        cards = Card.objects.filter(active=True).order_by('id')
        codes = Code.objects.filter(fk_user_id=self.kwargs['pk']).values('fk_card').distinct()
        context['codes'] = codes.count()
        context['total'] = cards.count()
        # context['percentage'] = codes.count() * 100 / cards.count()
        return context

    def get_queryset(self, *args, **kwargs):
        get_object_or_404(User, pk=self.kwargs['pk'])
        cards = Card.objects.filter(fk_department__slug=self.kwargs['slug'], is_badge=False, active=True).order_by('id')
        for card in cards:
            codes = Code.objects.filter(fk_user_id=self.kwargs['pk'], fk_card=card)
            if codes.exists():
                card.obtained = True
                card.codes = codes
        return cards
