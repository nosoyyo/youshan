import time

from utils import formatToday
from models import theGroup


def avr(l: list) -> float:
    return sum(l)/len(l)


def avrOrder(l: list) -> list:
    print(f'平均值：{avr(l)}')
    _list = sorted(list(zip([abs(i-avr(l)) for i in l], l)))
    return [i[1] for i in _list]


def buildLattice(day=formatToday()):
    '''
    Tell nth seconds of the day
    '''
    tup = (int(day[:4]), int(day[4:6]), int(day[6:8]), 0, 0, 0, 0, 0, 0)
    start = time.mktime(tup)
    n_lattice = int((time.time() - start) / 300)
    return [start + i*300 for i in range(n_lattice)]


def getTodayRange():
    test = {20180101: 1514736000}
    pass


def contrib(msg):
    group = theGroup(msg)
    # TODO
