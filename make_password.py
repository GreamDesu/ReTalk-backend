import string
from random import choice

Q = string.ascii_letters + string.digits


def make_password(num=10):
    return ''.join([choice(Q) for i in xrange(num)])

print make_password(25)
