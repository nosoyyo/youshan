import time

from models import User, theGroup
from utils import formatToday


def saveOnDisk(msg):
    '''
    Deprecated.
    Just for backward compatible
    TODO data migration
    '''
    group = theGroup(msg)
    bot = msg.bot

    def getNamePuidDict():
        bot.enable_puid()
        name_list = [m.nick_name for m in group.members]
        puid_list = [m.puid for m in group.members]
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
    TODO is transaction necessary?
    '''
    saveOnDisk(msg)
    recv_time = time.time()
    user = User(msg)
    user.group = theGroup(user.group)
    user.uuid = theGroup.getUserUUID(user)
    try:
        if user.r.hset(user.group.uuid, recv_time, msg.text):
            user.r.rpush(f'{user.uuid}{formatToday()}', recv_time)
            user.r.zincrby(f'{user.group.uuid}{formatToday()}freq', user.uuid)
            user.r.zincrby(
                f'{user.group.uuid}{formatToday()}freq', user.group.uuid)

        if msg.member.group.name != list(
                user.r.hvals('group_name_history'))[-1]:
            user.r.hset('group_name_history', recv_time, msg.member.group.name)

    except Exception as e:
        print(e)
