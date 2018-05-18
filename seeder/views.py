from card.models import Rarity, Department, Card
from random import randint
from django.http import HttpResponse
from django.contrib.auth.models import User


def populate_database(self):
    # check if the database was populated

    list_user = User.objects.all().count()
    if list_user < 20:
        for user in range(1, 21):
            user_save = User.objects.create_user('jason'+str(user), 'garcia.robertogarcia+'+str(user)+'@gmail.com', 'johnpassword'+str(user))
            user_save.is_staff = True
            user_save.save()

    list_rarity = Rarity.objects.all().count()
    if list_rarity < 3:
        rarity = ['low', 'medium', 'high']
        for value in rarity:
            r = Rarity(description=value)
            r.save()
        list_departments = Department.objects.all().count()

        departments = ['Management', 'Finance', 'Technology', 'Human', 'Resources']
        total_departments = len(departments)

        if list_departments <= total_departments:

            for value in departments:
                d = Department(description=value)
                d.save()

        list_cards = Card.objects.all().count()

        if list_cards < 200:
            for x in range(1, 200):
                c = Card(
                    name='name ' + str(x),
                    order=1,
                    description='description ' + str(x),
                    photo='http://static.pulzo.com/images/20180225220341/ficha-juan-cuadrado-896x485.jpg?itok=1519614733',
                    fk_rarity=Rarity.objects.get(id=randint(1, 3)),
                    fk_department=Department.objects.get(id=randint(1, total_departments))
                )
                c.save()

    return HttpResponse('Seed done')
