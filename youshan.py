import time
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
    corpus = getTodayCorpus()
    today_n = len(corpus)
    if not puid:
        sds = {}
        sd_names = list(youshan)
        sd_names.pop(0)
        sd_rank = {}
        for sd in sd_names:
            sds[sd] = [item for item in corpus if item['user'] is sd]
        for sd in sd_names:
            sd_rank[sd] = len(sds[sd])
        sd_rank = {value: key for key, value in sd_rank.items()}
        sd_rank = SortedDict(sd_rank)
        chart = '''今天贵群刷了{}条:
第一名：{} 老师 {} 条
第二名：{} 老师 {} 条
第三名：{} 老师 {} 条
第四名：{} 老师 {} 条
第五名：{} 老师 {} 条
第六名：{} 老师 {} 条        
第七名：{} 老师 {} 条'''.format(
            today_n,
            sd_rank[list(sd_rank)[-1]],
            list(sd_rank)[-1],
            sd_rank[list(sd_rank)[-2]],
            list(sd_rank)[-2],
            sd_rank[list(sd_rank)[-3]],
            list(sd_rank)[-3],
            sd_rank[list(sd_rank)[-4]],
            list(sd_rank)[-4],
            sd_rank[list(sd_rank)[-5]],
            list(sd_rank)[-5],
            sd_rank[list(sd_rank)[-6]],
            list(sd_rank)[-6],
            sd_rank[list(sd_rank)[-7]],
            list(sd_rank)[-7],
        )
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


def getTodayCorpus() -> list:
    '''
    return a list of dict like
    {'serial': '164',
    'user': 'ch',
    'date': '20180615',
    'time': 1528996039.0,
    'type': 'Text',
    'text': '回不来了，已经晚了'}
    '''
    with open('db', 'r') as f:
        all = f.read().split('\n')
    today = formatToday()
    return [eval(item.split(' = ')[1])
            for item in all if today in item.split(' = ')[0]]


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
    return [the_group.search(name)[0].puid for name in names]


@bot.register(Group, None, except_self=False)
def deal(msg):

    if msg.chat.puid == the_group.puid:
        print(msg)
        persistize(msg)

        if msg.is_at:
            queries = getQuery(msg)
            if not queries:
                the_group.send(stats())
            else:
                for query in queries:
                    # :query: `puid`: str
                    return stats(query)
