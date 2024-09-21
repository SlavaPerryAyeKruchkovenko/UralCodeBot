from models.Context import Context
from models.User import User
from scenarios.scenarios import Scenarios
from scenarios.nothingScenarios import NothingScenarios

def get_user_from_message(message, context: Context):
    t_id = message.from_user.id
    user = context.get_user_by_id(t_id)
    if user is None:
        user = User(message.from_user.username, t_id)
        context.add_user(user)
    return user


async def execute_scenarios(scenarios: Scenarios, user: User, bot, context, message):
    if scenarios != None:
        await scenarios.execute(message.text)
        await bot.send_message(user.get_id(), scenarios.message)
        if scenarios.is_finish:
            context.del_scenarios_by_user(user)
    else:
        newScenarios = NothingScenarios(message.chat.id)
        context.add_scenarios_by_user(user, NothingScenarios(message.chat.id))
        await execute_scenarios(newScenarios, user, bot, context, message)
