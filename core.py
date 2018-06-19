from datetime import datetime
from sortedcontainers import SortedDict

from core import getCorpus

youshan = {'group': '2082f7f0',
           'ly': '68a9c4c9',
           'ch': 'd328a12e',
           'shr': '0b4f46fa',
           'gc': '0a4b095f',
           'dg': '73b7c671',
           'hyh': 'd1adaecd',
           'bjh': '55d92152',
           }

the_group = bot.search(puid='2082f7f0')[0]


def getUserByPuid(puid: str) -> str:
    return tuple(youshan)[list(youshan.values()).index(puid)]


def formatToday() -> str:
    ahora = datetime.now()

    def zero(inp: int) -> str:
        if len(str(inp)) != 2:
            return '0' + str(inp)
        else:
            return str(inp)
    return str(ahora.year) + zero(ahora.month) + zero(ahora.day)


def genMsgId() -> str:
    with open('db', 'r') as f:
        return str(len(f.readlines()) + 1)


def groupKeyword(arg: str='today') -> str:
    corpus = ''
    if arg == 'today':
        corpus = getCorpus('raw_today')
    elif arg == 'alltime':
        corpus = getCorpus('raw_alltime')
    kw = jieba.analyse.textrank(
        corpus, topK=20, withWeight=False, allowPOS=('ns', 'n'))
    return '\n'.join(kw)


def persistize(msg):
    hoy = formatToday()
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
    print(msg_name + ' saved.')
    return True


def getQuery(msg: Message) -> list:
    '''
    return a list of puid: str, like
    ['01f0700d', 73b7c671']
    '''
    names = msg.text.replace('\u2005', '').split('@')[2:]
    if names:
        return [the_group.search(name)[0].puid for name in names]
    elif '\u2005' in msg.text:
        return msg.text.split('\u2005')[1]
    else:
        


def isPuid(queries):
    if isinstance(queries, list):
        for query in queries:
            if str(eval('0x'+query)).isdigit():
                return True
    else:
        return False


def getCorpus(arg='today', puid: str=None):
    '''
    :param `today`: `list` return a list of dict like
    {'serial': '164',
    'user': 'ch',
    'date': '20180615',
    'time': 1528996039.0,
    'type': 'Text',
    'text': '回不来了，已经晚了'}
    :param `raw_today`: `str` return everything people said today
    :param `raw_alltime`: `str` return everything people said since day0
    :param `raw_puid_today`: `str` return everything a certain people said today
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
        name = getUserByPuid(puid)
        return [item for item in corpus_today if item['user'] == name]
    elif arg == 'raw_puid_today':
        name = getUserByPuid(puid)
        user_corpus = [item for item in corpus_today if item['user'] == name]
        user_texts = [item['text']
                      for item in user_corpus if item['text'] is not None]
        return ''.join(user_texts)
