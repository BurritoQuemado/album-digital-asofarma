from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('prediccion/<int:id>', views.CreatePredictionView.as_view(), name='create_prediction'),
    # path('trivia', views.CreateTriviaView.as_view(), name='create_trivia'),
]
