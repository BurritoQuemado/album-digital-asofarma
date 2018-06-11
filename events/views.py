from django.views.generic.edit import CreateView
from .models import Match, Prediction
from .forms import PredictionForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class CreatePredictionView(SuccessMessageMixin, CreateView):
    template_name = 'events/create_prediction.html'
    form_class = PredictionForm
    success_url = reverse_lazy('home')
    success_message = 'Se ha enviado tu predicción con éxito'

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
