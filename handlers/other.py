from aiogram import Router, types, Bot
from aiogram.filters.command import Command
from aiogram.filters.chat_member_updated import LEAVE_TRANSITION, JOIN_TRANSITION, ChatMemberUpdatedFilter
from settings.db import UserDB

router = Router()

text = """
- Как пользоваться ботом?
- Сейчас расскажу. Сначала нужно добавить бота в канал и выдать ему все права.
Затем напишите <code>+админ @username</code> того кого хотите назначить админом(вместо @username, можно писать user id).
И всё теперь бот будет следить за модераторами которых вы назначили <b>этой командой</b>
"""

async def start(msg: types.Message):
    with UserDB() as db:
        user = db.get_user(msg.from_user.id)
        if not user:
            db.add_user(msg.from_user.id, msg.from_user.username or "", msg.from_user.full_name)
    await msg.answer(text=text, parse_mode="HTML")


async def leave(event: types.ChatMemberUpdated):
    with UserDB() as db:
        db.del_user(event.from_user.id)


async def join(event: types.ChatMemberUpdated):
    with UserDB() as db:
        if not db.get_user(event.from_user.id):
            db.add_user(event.from_user.id, event.from_user.username or "", event.from_user.full_name)


router.message.register(start, Command(commands=["help", "start"]))
router.my_chat_member.register(leave, ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION))
router.my_chat_member.register(join, ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))