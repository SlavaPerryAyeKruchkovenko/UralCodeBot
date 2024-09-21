from scenarios.scenarios import Scenarios

#Scenarious for not implemeted request
class NothingScenarios(Scenarios):
    _message:str = ""

    async def execute(self, data = None):
        self._message = "Неизвестная команда"
        
    @Scenarios.message.getter
    def message(self):
        return self._message

    @Scenarios.key_word.getter
    def key_word(self):
        return ""

    @Scenarios.is_finish.getter
    def is_finish(self) -> bool:
        return True