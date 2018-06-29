import time
from uuid import uuid4

from models import User, theGroup
from utils import formatToday


def saveOnDisk(msg):
    '''
    backward compatible
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


def persistize(msg):
    '''
    TODO Transaction
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
