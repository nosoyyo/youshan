import time
from wxpy import Bot, Group
from uuid import uuid4

from models import User, Query
from storage import persistize
from stats import stats, getTiming
from youshan import aloha, reLogin
from contribution import contrib


bot = Bot(cache_path=True, login_callback=aloha, logout_callback=reLogin)


def getTheGroup():
    '''
    TODO
    '''
    return bot.search('友善')[0]


def initGroup(group):
    '''
    Only call this when 1st time init a group, meanwhile no user has an uuid
    '''
    for member in group.members:
        user = User(member)
        user.uuid = user.r.hget(
            group.puid, user.nick_name) or uuid4().__str__()
        user.r.hset(group.puid, user.nick_name, user.uuid)
        user.r.hset(group.puid, user.uuid, user.nick_name)


@bot.register(Group, None, except_self=False)
def deal(msg):
    the_group = getTheGroup()
    if msg.chat.puid == the_group.puid:
        print(msg)
        persistize(msg)
        if msg.text is not None and '在吗' in msg.text:
            if Query.isCommand(msg):
                puid = the_group.search(Query.name)[0].puid
                the_group.send(getTiming(puid))
                return
        elif msg.is_at:
            time.sleep(0.5)
            query = Query(msg)
            if '我的统计' in query.command:
                the_group.send(stats(msg, User(msg)))
            elif '群统计' in query.command:
                the_group.send(stats(msg))
            elif '贡献值' in query.command:
                the_group.send(contrib(msg))
            else:
                time.sleep(0.5)
                the_group.send('你想干啥？')
