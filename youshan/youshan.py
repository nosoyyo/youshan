import time
from wxpy import Bot, Group
from uuid import uuid4

from models import User, Query, theGroup
from storage import persistize
from stats import stats, getTiming
from youshan import aloha, reLogin
from contribution import contrib


DGBUG = True
bot = Bot(cache_path=True, login_callback=aloha, logout_callback=reLogin)


def registerGroup(msg, cmd):
    group = theGroup(msg)
    if cmd == 'on':
        if all([m.is_friend for m in group.members]):
            if group.uuid not in group.r.lrange('registered_groups', 0, -1):
                if initGroup(group):
                    group.rpush('registered_groups', group.uuid)
                    return '已开启'
                else:
                    return '群初始化失败'
        else:
            return '只支持在全部群员均为好友的群里使用'
    elif cmd == 'off':
        pass


def getTheGroup(msg) -> theGroup:
    r = User(msg).r
    groups = bot.groups()
    target = set([int(i) for i in r.hvals('check_group')])
    for g in groups:
        # some tolerance on num of gmembers
        if 5 <= len(g.members) <= 10:
            friend_list = list(
                filter(lambda m: m.is_friend, [m for m in g.members]))
            hashes = set(hash(f.is_friend.name) for f in friend_list)
            # normally
            if len(hashes) == len(target & hashes):
                return theGroup(g)
            # num of gmembers changing
            elif len(hashes) != len(target & hashes):
                msg.member.group.send('[debug]检测到人数或昵称变更')
                return theGroup(g)


def initGroup(group):
    '''
    Only call this when 1st time init a group, meanwhile no user has an uuid
    '''
    for member in group.members:
        user = User(member)
        user.uuid = user.r.hget(
            group.uuid, user.nick_name) or uuid4().__str__()
        user.r.hset(group.uuid, user.nick_name, user.uuid)
        user.r.hset(group.uuid, user.uuid, user.nick_name)


@bot.register(Group, None, except_self=False)
def deal(msg):
    the_group = getTheGroup(msg)
    # register & init group
    # if msg.text == '开启统计功能':
    #     the_group.send(registerGroup(msg, 'on'))
    # elif msg.text == '关闭统计功能':
    #     the_group.send(registerGroup(msg, 'off'))

    if theGroup(msg.member.group) == the_group:
        print(msg)
        persistize(msg)
        if msg.text is not None and '在吗' in msg.text:
            if Query.isCommand(msg):
                msg.member.group.send(getTiming(User(msg)))
                return
        elif msg.is_at:
            time.sleep(0.5)
            query = Query(msg)
            if '我的统计' in query.command:
                msg.member.group.send(stats(msg, User(msg)))
            elif '群统计' in query.command:
                msg.member.group.send(stats(msg))
            elif '贡献值' in query.command:
                msg.member.group.send(contrib(msg))
            else:
                time.sleep(0.5)
                msg.member.group.send('你想干啥？')
