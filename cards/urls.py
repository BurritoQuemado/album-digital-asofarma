from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    # path('redeem/', views.AddCodeView.as_view(), name='redeem'),
    path('enviar/<str:code>/', views.SendCodeView.as_view(), name='send_code'),
    path('redeem/<str:code>/<str:email>/', views.EmailSaveView.as_view(), name='email_save'),
    path('<int:pk>/portada/', views.CoverView.as_view(), name='card_cover'),
    path('<int:pk>/<slug:slug>/', views.CardList.as_view(), name='card_list'),
]
