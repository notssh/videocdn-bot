import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
import consts
from aiogram.utils import markdown as md


async def test(message: types.Message):
    await message.reply(message.from_user.id)


async def start(message: types.Message):
    if consts.database_url is not None:
        from database import update_user_usage_count
        await update_user_usage_count(message.from_user.id, 'start')
    await message.reply(f'*Привет!*\n\n'
                        f'Этот бот позволяет искать любые фильмы, кино и сериалы на videocdn.tv. '
                        f'Также имеется поддержка инлайн-режима.\n'
                        f'Внимание! Это неофициальный бот, созданный и поддерживаемый энтузиастами. '
                        f'К проекту videocdn.tv не имеет никакого отношения, '
                        f'лишь использует его в качестве источника данных.\n\n'
                        f'Команды - /help', parse_mode=types.ParseMode.MARKDOWN)


async def about(message: types.Message):
    await message.reply(f'*О проекте*\n\n'
                        f'Это небольшой опенсорс-проект, созданный за пару дней.\n'
                        f'Бот написан на языке программирования Python 3 '
                        f'и использует для взаимодействия с Telegram библиотеку aiogram 2.\n'
                        f'{md.link("Исходный код доступен для всех желающих!", f"https://github.com/notssh/videocdn-bot/")}\n'
                        f'Например, Вы можете запустить у себя такого же бота, '
                        f'изучить как он устроен, сделать собственный форк с дополнительным функционалом!\n'
                        f'Если есть предложение по улучшению бота, '
                        f'или столкнулись с какими-либо проблемами при использовании - создайте issue на Github.\n'
                        f'Внимание! Это неофициальный бот, созданный и поддерживаемый энтузиастами. '
                        f'К проекту videocdn.tv не имеет никакого отношения, '
                        f'лишь использует его в качестве источника данных.', parse_mode=types.ParseMode.MARKDOWN)


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Отмена действия, перехожу в обычное состояние.", reply_markup=types.ReplyKeyboardRemove())


async def ping(message: types.Message):
    await message.reply(f"<b>Понг, {round((message.date.timestamp()-datetime.datetime.now().timestamp()), 2)} сек</b>",
                        parse_mode=types.ParseMode.HTML)


def register_dp(dp):
    # dp.register_message_handler(test, commands="test")
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(about, commands="about")
    dp.register_message_handler(ping, commands="ping")
    # dp.register_message_handler(cancel, commands="cancel", state="*")
