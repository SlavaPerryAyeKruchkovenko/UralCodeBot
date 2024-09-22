import os
from dotenv import load_dotenv
import logging
from scenarios.notAuthScenarios import NotAuthScenarios
from utils.botUtils import *

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart

from models.Context import Context
from scenarios.authScenarios import AuthScenarios
from scenarios.subscribeScenarios import SubscribeScenarios
import asyncio

load_dotenv()
token = os.getenv("token")
code = os.getenv("code")
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
context = Context()
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


@dp.message(Command("auth"))
@dp.message(CommandStart())
async def handle_auth(message: types.Message):
    user = get_user_from_message(message, context)
    scenarios = AuthScenarios(code, message.chat.id, user)
    context.add_scenarios_by_user(user, scenarios)
    await scenarios.execute()
    await bot.send_message(user.get_id(), scenarios.message)


@dp.message(Command("subscribe"))
async def subscribe_notify(message: types.Message):
    user = get_user_from_message(message, context)
    scenarios = (
        SubscribeScenarios(user, message.chat.id)
        if user.get_is_auth()
        else NotAuthScenarios(message.chat.id)
    )
    context.add_scenarios_by_user(user, scenarios)
    await scenarios.execute()
    await bot.send_message(user.get_id(), scenarios.message)
    if scenarios.is_finish:
        context.del_scenarios_by_user(user)


@dp.message(F.text)
async def handle_text(message):
    user = get_user_from_message(message, context)
    scenarios = context.get_scenraios_by_user(user)
    await execute_scenarios(scenarios, user, bot, context, message)

async def send_photo_for_subscribers(photo,message):
    for user in context.users:
        if user.get_is_subscribe():
            await bot.send_message(user.get_id(), message)
            await bot.send_photo(user.get_id(), photo)

async def init_bot() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    print("Notifier_CFaPP_bot is Started")


if __name__ == "__main__":
    asyncio.run(init_bot())
