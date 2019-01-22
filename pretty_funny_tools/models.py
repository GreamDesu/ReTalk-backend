# coding: utf-8
from django.db import models
from datetime import timedelta
from django.utils.timezone import now
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class FailAuthTry(models.Model):
    ip = models.GenericIPAddressField()
    try_time = models.DateTimeField(default=now())

    CRITICAL_FAIL_NUMBER = 10
    TIMEOUT = 1  # in minutes

    def save(self, *args, **kwargs):
        fails = FailAuthTry.objects.filter(ip=self.ip, try_time__gte=(now() - timedelta(hours=1))).count()
        if fails > FailAuthTry.CRITICAL_FAIL_NUMBER:
            try:
                locked_person = LockedObject.objects.get(ip=self.ip)
                locked_person.time_when_can_try_again = now() + timedelta(minutes=FailAuthTry.TIMEOUT)
                locked_person.save()
                FailAuthTry.objects.filter(ip=self.ip, try_time__gte=(now() - timedelta(hours=1))).delete()
            except LockedObject.DoesNotExist:
                LockedObject.objects.create(ip=self.ip)

        return super(FailAuthTry, self).save(*args, **kwargs)

    def __str__(self):
        return 'Authorisation from %s failed at %s' % (self.ip, self.try_time)

    class Meta:
        verbose_name = 'Auth fail'
        verbose_name_plural = 'Auth fails'


class LockedObject(models.Model):
    ip = models.GenericIPAddressField()
    time_when_can_try_again = models.DateTimeField(default=now())
