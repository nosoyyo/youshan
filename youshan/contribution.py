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
    for i in range(1, len(barriers), 1):
        a, b = barriers[i-1], barriers[i]
        if list_set_alls[a:b] not in shades:
            shades.append(list_set_alls[a:b])
    shades = [i for i in shades if len(i) > 1]
    return shades


def countShadeShowUps(shade: list):
    '''
    Count all the `show_up`s with in a certain shade

    :param shade: a `list` contains lattice nodes
    '''
    show_ups = 0
    for u in group.members:
        for key in u.show_ups:
            if key in shade:
                show_ups += 1
    return show_ups


def getBiggestShade(shades: list) -> tuple:
    '''
    Return a tuple of two elements
    :tuple[0]: a `list` of lattices, therefore a shade
    :tuple[1]: the score of the shade

    :param shades: `list` of a `list`
    '''
    result = {}
    for shade in shades:
        result.update({shade[0]: countShadeShowUps(shade)})
    key = [key for key in result.keys() if result[key] ==
           sorted(list(result.values()))[-1]][0]
    return ([i for i in shades if i and i[0] == key][0], result[key])


def contrib(msg):
    pass
