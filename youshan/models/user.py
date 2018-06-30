from .base import Base


class User(Base):
    '''
    accepts either msg or member as intake
    '''

    def __init__(self, intake):
        self.is_friend = None
        # assert hasattr `group`
        self.group = intake.group

        if hasattr(intake, 'member'):
            if intake.member.is_friend:
                member = intake.member.is_friend
                self.is_friend = True
            else:
                member = intake.member
        elif hasattr(intake, 'is_friend'):
            if intake.is_friend:
                member = intake.is_friend
                self.is_friend = True
            else:
                member = intake
        self.puid = member.puid
        self.name = member.name
        self.nick_name = member.nick_name

        if self.is_friend:
            self.city = member.city
            self.province = member.province
            self.gender = member.sex
            self.signature = member.signature

        if hasattr(member, 'display_name'):
            self.display_name = member.display_name

    def __repr__(self):
        return f'<User instance of {self.nick_name}, puid {self.puid}>'

    def getUUID(self):
        raise NotImplementedError
