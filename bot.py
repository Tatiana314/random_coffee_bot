from datetime import datetime

import asyncio

import pytz
from aiogram import Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import BotCommand

from bot_app.core.config import bot
from bot_app.database.engine import get_async_session, session_maker
from bot_app.handlers.admin import admin_router
from bot_app.handlers.base_commands import base_commands_router
from bot_app.handlers.callbacks_handler import callback_router

from bot_app.handlers.user_registration import user_reg_router
from bot_app.mailing.mailing import meeting_mailing, meeting_reminder_mailing
from bot_app.middleware.dp import DataBaseSession
from bot_app.mailing.distribution import distribution


async def on_startup():
    """Startup message."""
    print('Бот запущен')


async def on_shutdown():
    """Shutdown message."""
    print('Бот лег')


COMMANDS = [
        BotCommand(command="/start", description="Перезапустить бота"),
        BotCommand(command="/admin", description="Панель администратора"),
    ]


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(user_reg_router)
    dp.include_router(base_commands_router)
    dp.include_router(callback_router)
    dp.include_router(admin_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    timezone = pytz.timezone('Europe/Moscow')
    scheduler = AsyncIOScheduler(timezone=timezone)

    sql_session = await anext(get_async_session())
# ДЛЯ ТЕСТИРОВАНИЯ РАССЫЛКИ НА ПН НУЖНО РАЗКОММЕНТИРОВАТЬ СТРОКИ 42-43, РАССЫЛКА БУДЕТ ПРОИСХОДИТЬ ПРИ ЗАПУСКЕ БОТА
    scheduler.add_job(distribution, args=(sql_session,),
                      next_run_time=datetime.now())
    # scheduler.add_job(distribution, args=(sql_session,),
    #                   trigger='cron', day_of_week='thu', hour=19, minute=58)
    scheduler.add_job(distribution, args=(sql_session,),
                      trigger='cron', day_of_week='0-6', hour=10, minute=00)

# ДЛЯ ТЕСТИРОВАНИЯ РАССЫЛКИ НА ПТН НУЖНО РАЗКОММЕНТИРОВАТЬ СТРОКИ 48-49, РАССЫЛКА БУДЕТ ПРОИСХОДИТЬ ПРИ ЗАПУСКЕ БОТА
    # scheduler.add_job(meeting_reminder_mailing, args=(
    #     sql_session,), next_run_time=datetime.now())
    # scheduler.add_job(meeting_reminder_mailing, args=(sql_session,), trigger='cron',
    #                   day_of_week='thu', hour=19, minute=36)
    scheduler.add_job(meeting_reminder_mailing, args=(sql_session,), trigger='cron',
                      day_of_week='0-6', hour=12, minute=00)
    scheduler.start()
    await bot.set_my_commands(COMMANDS)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
