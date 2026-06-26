import asyncio
import sys
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import Update
from config import TELEGRAM_TOKEN
from database import init_db
from handlers.start import start_command
from handlers.meal import handle_text, handle_photo
from handlers.stats import stats_today
from handlers.profile import set_goal, show_goal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    await init_db()
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("today", stats_today))
    app.add_handler(CommandHandler("goal", set_goal))
    app.add_handler(CommandHandler("profile", show_goal))
    app.add_handler(CallbackQueryHandler(stats_today, pattern="stats_today"))
    app.add_handler(CallbackQueryHandler(show_goal, pattern="show_goal"))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    logger.info("Бот запущен!")
    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    await asyncio.Event().wait()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())