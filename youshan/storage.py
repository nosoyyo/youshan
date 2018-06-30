import time
from uuid import uuid4

from models import User, theGroup
from utils import formatToday


def saveOnDisk(msg):
    '''
    Deprecated.
    Just for backward compatible
    TODO data migration
    '''
    the_group = theGroup(msg)
    bot = msg.bot

    def getNamePuidDict():
        bot.enable_puid()
        name_list = [m.nick_name for m in the_group.members]
        puid_list = [m.puid for m in the_group.members]
        return dict(zip(name_list, puid_list))

    def getUserByPuid(puid: str) -> str:
        return tuple(getNamePuidDict())[
            list(getNamePuidDict().values()).index(puid)]

    hoy = formatToday()

    def genMsgId() -> str:
        with open('db', 'r') as f:
            return str(len(f.readlines()) + 1)

    serial = genMsgId()
    content = {}
    content['serial'] = serial
    content['user'] = getUserByPuid(msg.member.puid)
    content['date'] = hoy
    content['time'] = msg.create_time.timestamp()
    content['type'] = msg.type
    content['text'] = msg.text

    msg_name = 'msg{}_{}'.format(hoy, serial)
    with open('db', 'a') as f:
        f.write(msg_name + ' = ' + str(content) + '\n')
    print(msg_name + ' saved on disk.')
    return True


def getCorpus(arg='today', puid: str=None):
    '''
    Deprecated.
    Only use to get old data on local disk storage.

    :param `today`: `list` return a list of dict like
    {'serial': '164',
    'user': 'ch',
    'date': '20180615',
    'time': 1528996039.0,
    'type': 'Text',
    'text': '回不来了，已经晚了'}
    :param `raw_today`: `str` return everything people said today
    :param `raw_alltime`: `str` return everything people said since day0
    :param `raw_puid_today`: `str` return everything a certain dude said today
    '''
    with open('db', 'r') as f:
        all_dict = f.read().split('\n')
    all_dict.remove('')
    # today for instance: `20180615`
    today = formatToday()
    corpus_today = [eval(item.split(' = ')[1])
                    for item in all_dict if today in item.split(' = ')[0]]
    if arg == 'today':
        return corpus_today
    elif arg == 'raw_today':
        return ''.join(
            [item['text'] for item in corpus_today if item['text'] is not None])
    elif arg == 'raw_alltime':
        corpus_all = [eval(item.split(' = ')[1]) for item in all_dict]
        return ''.join(
            [item['text'] for item in corpus_all if item['text'] is not None])
    elif arg == 'puid_today':
        return [m for m in corpus_today if m['user'] == getUserByPuid(puid)]
    elif arg == 'raw_puid_today':
        name = getUserByPuid(puid)
        user_corpus = [item for item in corpus_today if item['user'] == name]
        user_texts = [item['text']
                      for item in user_corpus if item['text'] is not None]
        return ''.join(user_texts)


def persistize(msg):
    '''
    TODO Transaction
    TODO is transaction necessary?
    '''
    saveOnDisk(msg)
    recv_time = time.time()
    user = User(msg)
    try:
        if user.r.hset(user.group.puid, recv_time, msg.text):
            user.uuid = user.r.hget(
                user.group.puid, user.nick_name) or uuid4().__str__()
            user.r.hset(user.group.puid, user.nick_name, user.uuid)
            user.r.rpush(f'{user.uuid}{formatToday()}', recv_time)
            user.r.zincrby(f'{user.group.puid}{formatToday()}freq', user.uuid)
            user.r.zincrby(
                f'{user.group.puid}{formatToday()}freq', user.group.puid)
    except Exception as e:
        print(e)
