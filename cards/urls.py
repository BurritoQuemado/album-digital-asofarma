from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('', views.new_cards_save, name='index'),
    path('send/<slug:target>/', views.send_cards, name='send'),
    path('send/<slug:target>/<slug:department>', views.send_cards, name='send'),
    path('redeem/<slug:code>/<str:user>/', views.users_cards_save_email, name='redeem_email'),
    path('redeem/<slug:code>/', views.users_cards_save_session, name='redeem_session'),
]

# examples of use
# http://127.0.0.1:8000/card/send/department/Testing
