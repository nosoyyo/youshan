from uuid import uuid4

from .base import Base
from .user import User


class theGroup(Base):
    '''
    accepts either msg or Group as intake
    '''
    uuid = '1a8ac0f3-dfed-4b35-a00d-5eca7312b8db'

    def __init__(self, intake):

        if not hasattr(intake, 'owner'):
            intake = intake.member.group
        self.puid = intake.puid
        self.name = intake.name
        self.nick_name = intake.nick_name
        self.owner = User(intake.owner)

        if len(intake.members) > 0:
            self.raw_members = intake.members
            self.members = [User(m) for m in intake.members]

        for user in self.members:
            user.group = self

    def __repr__(self):
        return f'<theGroup instance of {self.nick_name}>'

    def __eq__(self, obj):
        return self.raw_members == obj.raw_members

    @classmethod
    def getTheGroup(cls, msg):
        r = cls.r
        groups = msg.bot.groups()
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

    @classmethod
    def registerGroup(cls, msg, cmd):
        group = theGroup(msg)
        if cmd == 'on':
            if all([m.is_friend for m in group.members]):
                if group.uuid not in group.r.lrange(
                        'registered_groups', 0, -1):
                    if cls.initGroup(group):
                        group.rpush('registered_groups', group.uuid)
                        return '已开启'
                    else:
                        return '群初始化失败'
            else:
                return '只支持在全部群员均为好友的群里使用'
        elif cmd == 'off':
            pass

    def initGroup(self, group):
        '''
        Only call this when 1st time init a group,
        meanwhile no user has an uuid
        '''
        for member in group.members:
            user = User(member)
            user.uuid = user.r.hget(
                group.uuid, user.nick_name) or uuid4().__str__()
            user.r.hset(group.uuid, user.remark_name, user.uuid)
            user.r.hset(group.uuid, user.uuid, user.remark_name)

    @classmethod
    def getUserUUID(cls, user) -> str:
        # self.group need to be dynamically loaded
        user.uuid = cls.r.hget(cls.uuid, user.remark_name)
        return user.uuid
