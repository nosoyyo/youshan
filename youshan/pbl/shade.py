import time
from functools import reduce

from utils import formatToday


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


def getStartSecOfTheDay(day: str='today') -> float:
    if day is 'today':
        day = formatToday()
    tup = (int(day[:4]), int(day[4:6]), int(day[6:8]), 0, 0, 0, 0, 0, 0)
    return time.mktime(tup)


def buildLattice(day: str='today') -> list:
    '''
    :param day: like `20180705`
    '''
    if day is 'today':
        day = formatToday()
    start = getStartSecOfTheDay(day)
    n_lattice = int((time.time() - start) / 300)
    return [start + i*300 for i in range(n_lattice)]


def getSecByLattice(lattice: int, day: str='today') -> float:
    '''

    :param lattice: `int`, range(288)
    '''
    if lattice in range(288):
        if day is 'today':
            day = formatToday()
        start = getStartSecOfTheDay(day)
        return start + lattice*300


def buildShades(group, day: str='today'):

    # every user's show_ups in their lists respectively
    alls = list(map(lambda x: countUserShowUps(
        x, day), [user for user in group.members]))
    # every user's show_ups in one big list
    # (lame use of `reduce` but works well)
    alls = reduce(lambda a, b: a+b, alls)
    list_set_alls = sorted(list(set(alls)))

    # find barriers of each shade
    barriers = []
    for i in range(len(list_set_alls)-2):
        if list_set_alls[i+1]-list_set_alls[i] > 1:
            barriers.append(i+1)

    # find all shades
    shades = []
    for i in range(1, len(barriers), 1):
        if i == 1:
            a, b = 0, barriers[i-1]
        else:
            a, b = barriers[i-1], barriers[i]
        if list_set_alls[a:b] not in shades:
            shades.append(list_set_alls[a:b])
    shades = [i for i in shades if len(i) > 1]
    return shades


def countUserShowUps(user, day: str='today') -> list:
    '''
    Return a `list` of all the lattices a user has appeared
    '''
    if day is 'today':
        day = formatToday()

    user.buildUserCorpus(day)
    lattices = buildLattice(day)
    # :key: `timestamp`
    user.show_ups = [lattices.index(
        [i for i in lattices if i < key][-1]) for key in user.corpus_keys]
    return user.show_ups


def countShadeShowUps(group, shade: list):
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


def getBiggestShade(group, shades: list) -> tuple:
    '''
    Return a tuple of two elements
    :tuple[0]: a `list` of lattices, therefore a shade
    :tuple[1]: the score of the shade

    :param shades: `list` of a `list`
    '''
    result = {}
    for shade in shades:
        result.update({shade[0]: countShadeShowUps(group, shade)})
    key = [key for key in result.keys() if result[key] ==
           sorted(list(result.values()))[-1]][0]
    return ([i for i in shades if i and i[0] == key][0], result[key])


def getLongestShade(group, shades: list) -> tuple:
    '''
    Return a `tuple` of two elements
    :tuple[0]: a `list` of lattices, therefore a shade
    :tuple[1]: the score of the shade

    :param shades: `list` of `list` of `lattice`
    '''
    result = {}
    for shade in shades:
        result.update({shade[0]: len(shade)})
    key = [key for key in result.keys() if result[key] ==
           sorted(list(result.values()))[-1]][0]
    shade = [i for i in shades if i and i[0] == key][0]
    return (shade, countShadeShowUps(group, shade))


def getShadeParticipants(group, shade: list) -> dict:
    '''
    Return a `list` of `tuple` of two elements
    :tuple[0]: `User` take part in `shade`
    :tuple[1]: how many times he participated

    :param group: `theGroup` instance
    :param shade: `list` of `lattice`
    '''
    participants = []
    for lattice in shade:
        for u in group.members:
            if lattice in u.show_ups:
                participants.append(u)

    return list(set([(i, participants.count(i)) for i in participants]))
