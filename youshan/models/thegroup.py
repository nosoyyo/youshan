from .base import Base
from .user import User


class theGroup(Base):
    '''
    accepts either msg or Group as intake
    '''

    def __init__(self, intake):

        if not hasattr(intake, 'owner'):
            intake = intake.member.group
        self.uuid = '1a8ac0f3-dfed-4b35-a00d-5eca7312b8db'
        self.puid = intake.puid
        self.name = intake.name
        self.nick_name = intake.nick_name
        self.owner = User(intake.owner)

        if len(intake.members) > 0:
            self.raw_members = intake.members
            self.members = [User(m) for m in intake.members]

    def __repr__(self):
        return f'<theGroup instance of {self.nick_name}, puid {self.puid}>'

    def __eq__(self, obj):
        return self.raw_members == obj.raw_members
