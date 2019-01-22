from django.core.management import BaseCommand
from rest_framework.authtoken.models import Token

from api import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        q = 0
        for usr in models.User.objects.all():
            obj, created = Token.objects.get_or_create(user=usr)
            if created:
                q += 1

        print 'Done. %d tokens created' % q
