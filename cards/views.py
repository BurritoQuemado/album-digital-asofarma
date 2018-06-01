import base64
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from .forms import EmailSaveForm, AddCodeForm
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
        return reverse('cards:card_cover', kwargs={'pk': self.request.user.id})

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
class AddCodeView(SuccessMessageMixin, FormView):
    template_name = 'cards/card_save_form.html'
    form_class = AddCodeForm
    success_url = reverse_lazy('cards:redeem')
    success_message = "Se ha guardado la carta en tu álbum"

    def form_valid(self, form):
        user = self.request.user
        code = Code.objects.get(code=form.cleaned_data['code'])
        code.fk_user = user
        code.save()
        return super().form_valid(form)


class CoverView(DetailView):
    model = User
    template_name = 'cards/card_cover.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cards = Card.objects.all().order_by('id')
        codes = Code.objects.filter(fk_user_id=self.kwargs['pk']).values('fk_card').distinct()
        context['codes'] = codes.count()
        context['total'] = cards.count()
        return context


class CardList(ListView):
    template_name = 'cards/cards_list.html'
    model = Card
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department'] = Department.objects.get(slug=self.kwargs['slug'])
        badge = Card.objects.get(fk_department__slug=self.kwargs['slug'], is_badge=True)
        badge_codes = Code.objects.filter(fk_user_id=self.kwargs['pk'], fk_card=badge)
        if badge_codes.exists():
            badge.obtained = True
            badge.codes = badge_codes
        context['badge'] = badge
        context['user'] = User.objects.get(pk=self.kwargs['pk'])
        cards = Card.objects.all().order_by('id')
        codes = Code.objects.filter(fk_user_id=self.kwargs['pk']).values('fk_card').distinct()
        context['codes'] = codes.count()
        context['total'] = cards.count()
        # context['percentage'] = codes.count() * 100 / cards.count()
        return context

    def get_queryset(self, *args, **kwargs):
        get_object_or_404(User, pk=self.kwargs['pk'])
        cards = Card.objects.filter(fk_department__slug=self.kwargs['slug'], is_badge=False).order_by('id')
        for card in cards:
            codes = Code.objects.filter(fk_user_id=self.kwargs['pk'], fk_card=card)
            if codes.exists():
                card.obtained = True
                card.codes = codes
        return cards
