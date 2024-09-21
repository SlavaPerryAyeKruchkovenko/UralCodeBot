from models.User import User
from scenarios.scenarios import Scenarios


# Scenarious for auth use
class AuthScenarios(Scenarios):
    _get_code: bool = False
    _enter_code: bool = False
    _message: str = ""
    _available_code: str
    _number_of_attempts = 5
    _user: User = None

    def __init__(self, code, chat_id, user: User):
        super().__init__(chat_id)
        self._available_code = code
        self._user = user

    async def execute(self, data=None):
        if self._user.get_is_auth():
            self._get_code = True
            self._enter_code = True
            self._message = "Вы уже авторизовались"
        else:
            if not self._get_code:
                self._message = "Введите код доступа в формате 'dddddd' для получения уведомлений о нарушении мер безопастности"
                self._get_code = True
            elif not self._enter_code:
                if data == str(self._available_code):
                    self._enter_code = True
                    self._message = "Вы успешно авторизовались"
                    self._user.set_is_auth(True)
                elif self._number_of_attempts > 1:
                    self._number_of_attempts -= 1
                    self._message = f"Неверный код доступа, попыток осталось {self._number_of_attempts}"
                else:
                    self._number_of_attempts -= 1
                    self._message = f"Вы исчерпали все свои попытки"
            else:
                raise Exception("inccorrect state of scenarious")

    @Scenarios.message.getter
    def message(self):
        return self._message

    @Scenarios.key_word.getter
    def key_word(self):
        return "auth"

    @Scenarios.is_finish.getter
    def is_finish(self) -> bool:
        return self._number_of_attempts <= 0 or (self._get_code and self._enter_code)
