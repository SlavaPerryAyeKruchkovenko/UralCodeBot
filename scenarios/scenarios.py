from abc import ABC, abstractmethod

class Scenarios:
    """Abstract Scenarios"""
    _chat_id: str
    
    def __init__(self, chat_id):
        self._chat_id = chat_id

    @abstractmethod
    async def execute(self, data):
        pass

    @property
    def message(self) -> str:
        pass

    @property
    def key_word(self) -> str:
        pass

    @property
    def is_finish(self) -> bool:
        pass
