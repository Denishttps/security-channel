from aiogram import Bot, F, types, Router, Bot
from aiogram.filters.command import CommandObject, Command
from settings.db import UserDB
from settings.button import promt_btn
import asyncio

router = Router()


async def promote(msg: types.Message, bot: Bot, command: CommandObject):
    if command.args:
        admins = await bot.get_chat_administrators(msg.chat.id)
        adm_list = [(i.status, i.user.id, i.can_promote_members, i.user.is_bot) for i in admins]
        
        with UserDB() as db:
            if command.args.startswith("@"):
                user_list = db.get_user(username=command.args[1:])
            else:
                user_list = db.get_user(user_id=int(command.args))

            if user_list:
                user = user_list[0]
                for j in adm_list:
                    try:
                        if (j[0] == "creator" or j[2]) and not j[3]:
                            await bot.send_message(
                                chat_id=j[1],
                                text=
                                f"Вы точно хотите назначить администратором пользователя <a href='tg://user?id={user[1]}'>{user[3]}</a>",
                                reply_markup=promt_btn(str(msg.chat.id), str(user[1])))
                            await msg.delete()
                    except Exception as ex:
                        print(ex)
                        print(user)
            else:
                m = await msg.answer(
                    "Пользователь не заригестрирован в боте, попросите его отправить боту /start"
                )
                await asyncio.sleep(5)
                await msg.delete()
                await bot.delete_message(msg.chat.id, m.message_id)

async def callback_promt(call: types.CallbackQuery, bot: Bot):
    await call.answer()
    chat_id, user_id = call.data.rsplit("-", maxsplit=1)
    await bot.promote_chat_member(int(chat_id), int(user_id), can_post_messages=True)
    await call.message.edit_text("Пользователь назначен админом!")

async def not_callback_promt(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()



router.callback_query.register(not_callback_promt, F.data == "No")
router.callback_query.register(callback_promt)
router.channel_post.register(promote, Command(commands="админ", ignore_case=True, prefix="+/!."))
