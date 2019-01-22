# coding: utf-8
import math

from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware, get_current_timezone


def get_longitude_delta(current_latitude, r=1):
    """  Returns how many longitude degrees in r km at current_latitude """

    return abs(r / (111.3 * math.cos(current_latitude)))


def aware_now():
    """ Returns date and time now with current timezone """

    return make_aware(datetime.now(), get_current_timezone())


def td_in_minutes(td):
    """ Returns number of full minutes in timedelta
    Args:
        td - datetime.timedelta instance
    """

    return td.seconds // 60
