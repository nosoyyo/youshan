from .base import Base


class User(Base):
    '''
    accepts either msg or member as intake
    '''

    def __init__(self, intake):
        self.is_friend = False

        # intake: msg
        if hasattr(intake, 'member'):
            self.group = intake.member.group
            if intake.member.is_friend:
                member = intake.member.is_friend
                self.is_friend = True
            else:
                member = intake.member
        # intake: member
        elif hasattr(intake, 'is_friend'):
            self.group = intake.group
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
            if member.is_friend.remark_name:
                self.remark_name = member.is_friend.remark_name
            else:
                member.is_friend.set_remark_name(member.nick_name)
                self.remark_name = member.nick_name

        if hasattr(member, 'display_name'):
            self.display_name = member.display_name

    def __repr__(self):
        return f'<User instance of {self.nick_name}>'
