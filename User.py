from flask_login import UserMixin
import utils

class User(UserMixin):

    def __init__(self, username, active = True):
        results = utils.utils.readFromUserDB(username)
        self.__init__(results['id'],results['username'],results['mail'], active)


    def __init__(self, id, username, mail, active = True):
        self.id = id
        self.name = username
        self.mail = mail
        self.active = active


    def get_id(self):
        return self.id

    @property
    def is_active(self):
        return self.is_active