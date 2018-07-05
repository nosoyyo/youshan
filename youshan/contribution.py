import time
from functools import reduce

from utils import formatToday
from models import theGroup


def avr(l: list) -> float:
    '''
    :param l: any `list` contains only `int` of `float`
    '''
    return sum(l)/len(l)


def avrOrder(l: list) -> list:
    '''
    Return a `list` starts from the closest element
    to the avr value of the `list`

    :param l: any `list` contains only `int` of `float`
    '''
    print(f'平均值：{avr(l)}')
    _list = sorted(list(zip([abs(i-avr(l)) for i in l], l)))
    return [i[1] for i in _list]


def buildLattice(day: str=formatToday()):
    '''
    :param day: like `20180705`
    '''
    tup = (int(day[:4]), int(day[4:6]), int(day[6:8]), 0, 0, 0, 0, 0, 0)
    start = time.mktime(tup)
    n_lattice = int((time.time() - start) / 300)
    return [start + i*300 for i in range(n_lattice)]


def countUserShowUps(user) -> list:
    '''
    Return a `list` of all the lattices a user has appeared
    '''
    user.buildUserCorpus()
    lattices = buildLattice()
    user.show_ups = [lattices.index(
        [i for i in lattices if i < key][-1]) for key in user.corpus_keys]
    return user.show_ups


def buildShades(msg):
    group = theGroup(msg)
    barriers = []

    # every user's show_ups in their lists respectively
    alls = list(map(countUserShowUps, [user for user in group.members]))
    # every user's show_ups in one big list
    # (lame use of `reduce` but works well)
    alls = reduce(lambda a, b: a+b, alls)
    # counts = [alls.count(i) for i in set(alls)]
    list_set_alls = sorted(list(set(alls)))
    # find barriers of each shade
    for i in range(len(list_set_alls)-2):
        if list_set_alls[i+1]-list_set_alls[i] > 1:
            barriers.append(i+1)

    # find all shades
    shades = []
    for i in range(1, len(barriers), 2):
        a, b = barriers[i-1], barriers[i]
        if list_set_alls[a:b] not in shades:
            shades.append(list_set_alls[a:b])
    return shades

    def countShadeShowups(shade: list):
        pass

    def countShade(shades):
        # count show_ups in each shade
        shade_counts = {}
        for shade in shades:
            if shade:
                s = sum([alls.count(show_up) for show_up in shade if show_up])
                shade_counts.update({shade[0]: s})

        # find the biggest shade
        biggest_shade_starts_at = [i for i in shade_counts.keys(
        ) if shade_counts[i] == sorted(shade_counts.values())[-1]][0]

        biggest_shade = [i for i in shades if i and i[0]
                         == biggest_shade_starts_at][0]


def contrib(msg):
    pass
