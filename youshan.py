import time
import jieba.analyse
from datetime import datetime
from sortedcontainers import SortedDict

from wxpy import *

global LOGGEDIN
LOGGEDIN = False


def aloha():
    global LOGGEDIN
    LOGGEDIN = True
    print('successfully logged in')
    print('LOGGEDIN is ' + str(LOGGEDIN))


def reLogin():
    global LOGGEDIN
    LOGGEDIN = False
    print('logged out')
    print('LOGGEDIN is ' + str(LOGGEDIN))
    time.sleep(1)
    for i in range(3):
        bot = Bot(cache_path=True, login_callback=aloha,
                  logout_callback=reLogin)
        if LOGGEDIN:
            break


bot = Bot(cache_path=True, login_callback=aloha, logout_callback=reLogin)
bot.enable_puid()

youshan = {'group': '2082f7f0',
           'ly': '68a9c4c9',
           'ch': 'd328a12e',
           'shr': '0b4f46fa',
           'gc': '01f0700d',
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


def stats(puid: str=None) -> str:
    corpus = getCorpus('today')
    today_n = len(corpus)
    if not puid:
        sds = {}
        sd_names = list(youshan)
        sd_names.pop(0)
        sd_rank = {}
        for sd in sd_names:
            sds[sd] = [item for item in corpus if item['user'] is sd]
            sd_rank[sd] = len(sds[sd])
        sd_rank = {value: key for key, value in sd_rank.items()}
        sd_rank = SortedDict(sd_rank)

        # build chart
        chart_title = '今天贵群刷了{}条:\n'.format(today_n)
        charts = []
        sd_rank_list = list(sd_rank)
        sd_name_list = list(sd_rank.values())
        for i in range(len(sd_names)):
            chart_content = '#{} {} 老师 {} 条'.format(
                i+1, sd_name_list.pop(), sd_rank_list.pop())
            charts.append(chart_content)
        chart = chart_title + '\n'.join(charts)
        return chart
    elif puid:
        name = getUserByPuid(puid)
        user_corpus = [item for item in corpus if item['user'] == name]
        user_n = len(user_corpus)
        user_texts = [item['text']
                      for item in user_corpus if item['text'] is not None]
        max_chars = ''
        for item in user_texts:
            if len(item) > len(max_chars):
                max_chars = item

        user_chars = sum(len(item) for item in user_texts)
        stats = '''{} 老师今天刷了 {} 条，共 {} 字
平均每条 {:.2f} 字
最长一条 {} 字，内容如下：
{}
        '''.format(name, user_n, user_chars, user_chars/user_n,
                   len(max_chars), max_chars)
        return stats


def getCorpus(arg='today'):
    '''
    :param `today`: `list` return a list of dict like
    {'serial': '164',
    'user': 'ch',
    'date': '20180615',
    'time': 1528996039.0,
    'type': 'Text',
    'text': '回不来了，已经晚了'}
    :param `raw_today`: `str` return a str of everything people said
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
    else:
        return msg.text.split(' ')[1]


@bot.register(Group, None, except_self=False)
def deal(msg):

    if msg.chat.puid == the_group.puid:
        print(msg)
        persistize(msg)

        if msg.is_at:
            queries = getQuery(msg)
            if not queries:
                the_group.send(stats())
            elif '今日关键词' in queries:
                the_group.send(groupKeyword('today'))
            elif '全部关键词' in queries:
                the_group.send(groupKeyword('alltime'))
            elif '我的统计' in queries:
                the_group.send(stats(msg.member.puid))
            elif '群统计' in queries:
                the_group.send(stats())
            else:
                for query in queries:
                    # :query: `puid`: str
                    return stats(query)
