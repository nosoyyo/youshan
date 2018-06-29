from .base import Base
from .user improt User


class theGroup(Base):
    '''
    accepts either msg or Group as intake
    '''

    def __init__(self, intake):

        if not hasattr(intake, 'owner'):
            intake = intake.member.group

        self.puid = intake.puid
        self.name = intake.name
        self.nick_name = intake.nick_name
        self.owner = User(intake.owner)

        if len(intake.members) > 0:
            self.members = [User(m) for m in intake.members]

    def __repr__(self):
        return f'<theGroup instance of {self.nick_name}, puid {self.puid}>'
