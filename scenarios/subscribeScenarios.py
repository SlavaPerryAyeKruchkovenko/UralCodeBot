from models.User import User
from scenarios.scenarios import Scenarios

#Scenarious for subscribe user on notification
class SubscribeScenarios(Scenarios):
    _message:str = ""
    _user: User = None
    
    def __init__(self, user, chat_id):
        super().__init__(chat_id)
        self._user = user
        
    async def execute(self, data = None):
        if self._user != None:
            if self._user.get_is_subscribe():
                self._message = "Вы уже получаете информацию о происшествиях на предприятии"
            else:
                self._user.set_is_subscrive(True)
                self._message = "Успешно, теперь вы будете получать информацию о происшествиях на предприятии"
        else:
            raise Exception("user not defind")
                
        
    @Scenarios.message.getter
    def message(self):
        return self._message

    @Scenarios.key_word.getter
    def key_word(self):
        return "subscribe"

    @Scenarios.is_finish.getter
    def is_finish(self) -> bool:
        return True
    