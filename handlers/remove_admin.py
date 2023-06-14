from aiogram import Bot, Router, types
from aiogram.filters.chat_member_updated import KICKED, ChatMemberUpdatedFilter

router = Router()

async def check_user_status(event: types.ChatMemberUpdated, bot: Bot):
    try:
        await bot.promote_chat_member(event.chat.id, event.from_user.id, can_manage_chat=False)
        await bot.send_message(event.chat.id, text=f"Внимание! Админ <a href='tg://user?id={event.from_user.id}'>{event.from_user.full_name}</a> удалил пользователя с канала! Подробнее смотрите в недавних действиях. Я лишил его прав админимтратора, прошу вас во всем разобраться, будте осторожны!!!")
    except:
        pass


router.chat_member.register(check_user_status, ChatMemberUpdatedFilter(member_status_changed=KICKED))