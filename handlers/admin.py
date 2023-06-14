from aiogram import Router, types, F
from settings.db import UserDB
from aiogram.filters.command import Command, CommandObject

router = Router()
owner = 827521748

async def users_count(msg: types.Message) -> None:
    with UserDB() as db:
        count = db.get_all_users_count()
        await msg.answer(f"Количество пользователей бота: {count[0][0]}")

async def get_user_data(msg: types.Message, command: CommandObject) -> None:
    with UserDB() as db:
        try:
            user = db.get_user(user_id=int(command.args[1:]))
            if user:
                await msg.answer(f"Данные пользователя:\nId: <code>{user[0][1]}</code>\nUsername: @{user[0][2]}\nFull name: {user[0][3]}")
        except:
            await msg.answer("Error")


router.message.register(users_count, F.from_user.id == owner, Command(commands="users", prefix="!/."))
router.message.register(get_user_data, F.from_user.id == owner, Command(commands="user", prefix="!/."))