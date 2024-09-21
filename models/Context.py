from models.User import User
from scenarios.scenarios import Scenarios

class Context:
    users = []
    dictionary = {}

    def get_user_by_id(self,user_id):
        filterUsers = [u for u in self.users if u.get_id() == user_id]
        return filterUsers[0] if len(filterUsers) > 0 else None
    
    def add_user(self,user:User):
        filterUsers = [u for u in self.users if u.get_id() == user.get_id()]
        if len(filterUsers) <= 0:
            self.users.append(user) 

    def add_scenarios_by_user(self,user:User, scenarios: Scenarios):
        self.dictionary[user.get_id()] = scenarios

    def del_scenarios_by_user(self, user:User):
        del self.dictionary[user.get_id()]
    
    def get_scenraios_by_user(self, user:User) -> Scenarios:
        return self.dictionary.get(user.get_id())
