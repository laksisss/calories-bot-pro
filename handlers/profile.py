from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy import select
from database import async_session
from models import User, Goal

async def set_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if len(context.args) != 4:
        await update.message.reply_text("Формат: /goal 2000 100 70 250")
        return
    try:
        calories, protein, fat, carbs = map(float, context.args)
    except ValueError:
        await update.message.reply_text("Укажите числа")
        return
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == user.id))
        db_user = result.scalar_one()
        result = await session.execute(select(Goal).where(Goal.user_id == db_user.id))
        goal = result.scalar_one()
        goal.calories = calories
        goal.protein = protein
        goal.fat = fat
        goal.carbs = carbs
        await session.commit()
    await update.message.reply_text(
        f"✅ Цель: {calories:.0f} ккал | Б:{protein:.0f} Ж:{fat:.0f} У:{carbs:.0f}"
    )

async def show_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == user.id))
        db_user = result.scalar_one()
        result = await session.execute(select(Goal).where(Goal.user_id == db_user.id))
        goal = result.scalar_one()
    text = f"🎯 Цель:\n🔥 {goal.calories:.0f} ккал\n🥩 {goal.protein:.0f}г\n🥑 {goal.fat:.0f}г\n🍞 {goal.carbs:.0f}г"
    if update.callback_query:
        await update.callback_query.edit_message_text(text)
    else:
        await update.message.reply_text(text)