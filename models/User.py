class User:

    _id = 0
    _name = ""
    _is_auth = False
    _is_subscribe = False

    def __init__(self, username, t_id):
        self._name = username
        self._id = t_id

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_is_auth(self):
        return self._is_auth

    def get_is_subscribe(self):
        return self._is_subscribe

    def set_is_subscrive(self, value: bool):
        self._is_subscribe = value

    def set_is_auth(self, value: bool):
        self._is_auth = value
