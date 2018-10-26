from django.views.generic.edit import CreateView
from django.views.generic import FormView
from .models import Match, Prediction, Trivia
from django.db.models.query import QuerySet
from .forms import PredictionForm, TriviaForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
decorators = [login_required]


@method_decorator(decorators, name='dispatch')
class CreatePredictionView(SuccessMessageMixin, CreateView):
    template_name = 'events/create_prediction.html'
    form_class = PredictionForm
    success_url = reverse_lazy('home')
    success_message = 'Se ha enviado tu registrado con éxito'

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(CreatePredictionView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['id'] = self.kwargs['id']
        return form_kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        match = Match.objects.get(id=self.kwargs['id'])
        self.object.user = self.request.user
        self.object.match = match
        self.object.home_result = form.cleaned_data['home_result']
        self.object.away_result = form.cleaned_data['away_result']
        self.object.submitted = True
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            prediction = Prediction.objects.get(user=self.request.user, match_id=self.kwargs['id'], submitted=True)
            context['prediction_exists'] = prediction
        except Prediction.DoesNotExist:
            context['prediction_exists'] = None
        context['match'] = Match.objects.get(id=self.kwargs['id'])
        return context


@method_decorator(decorators, name='dispatch')
class CreateTriviaView(SuccessMessageMixin, FormView):
    template_name = 'events/create_trivia.html'
    form_class = TriviaForm
    success_url = reverse_lazy('home')
    success_message = 'Se ha enviado tu trivia con éxito'

    def form_valid(self, form):
        self.object = Trivia(user=self.request.user)
        self.object.save()
        for field in form.cleaned_data:
            responses = form.cleaned_data.get(field)
            if isinstance(responses, QuerySet):
                for response in responses:
                    self.object.options.add(response)
            else:
                self.object.options.add(responses)
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            trivia = Trivia.objects.get(user=self.request.user)
            context['trivia_exists'] = trivia
        except Trivia.DoesNotExist:
            context['trivia_exists'] = None
        return context
