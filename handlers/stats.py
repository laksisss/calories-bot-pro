from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from sqlalchemy import select, func
from database import async_session
from models import User, Meal, Goal

async def stats_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    today = datetime.now().strftime("%Y-%m-%d")
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == user.id))
        db_user = result.scalar_one()
        result = await session.execute(
            select(func.sum(Meal.calories), func.sum(Meal.protein),
                   func.sum(Meal.fat), func.sum(Meal.carbs))
            .where(Meal.user_id == db_user.id, Meal.date == today)
        )
        totals = result.one()
        calories = totals[0] or 0
        protein = totals[1] or 0
        fat = totals[2] or 0
        carbs = totals[3] or 0
        result = await session.execute(select(Goal).where(Goal.user_id == db_user.id))
        goal = result.scalar_one()
        progress = min(100, int((calories / goal.calories) * 100)) if goal.calories else 0
        text = (
            f"📊 Сегодня\n\n"
            f"🔥 {calories:.0f}/{goal.calories:.0f} ккал ({progress}%)\n"
            f"{'█' * (progress // 10)}{'░' * (10 - progress // 10)}\n\n"
            f"🥩 Белки: {protein:.0f}/{goal.protein:.0f}г\n"
            f"🥑 Жиры: {fat:.0f}/{goal.fat:.0f}г\n"
            f"🍞 Углеводы: {carbs:.0f}/{goal.carbs:.0f}г"
        )
    if update.callback_query:
        await update.callback_query.edit_message_text(text)
    else:
        await update.message.reply_text(text)