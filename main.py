from aiogram import Bot, Dispatcher
from handlers import remove_admin, promote, other, admin
from run import keep_alive
import os, asyncio

bot = Bot(token=os.environ['token'], parse_mode="HTML")
dp = Dispatcher()


#router
dp.include_router(remove_admin.router)
dp.include_router(promote.router)
dp.include_router(other.router)
dp.include_router(admin.router)

async def main():
    print("Bot started")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    keep_alive()
    asyncio.run(main())