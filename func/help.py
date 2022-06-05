from aiogram import types


async def main_help(message: types.Message):
    await message.reply(f'<b>Помощь по боту</b>\n\n'
                        f'<b>Поиск кино и сериалов</b>\n'
                        f'/search - быстрый поиск фильмов/сериалов. '
                        f'Используйте инлайн-кнопки под сообщением для выбора медиа и навигации\n\n'
                        f'<b>Использование в инлайн-режиме</b>\n'
                        f'Просто введите '
                        f'"@{(await message.bot.get_me()).username} [название фильма/сериала]" в любом чате '
                        f'и выберите нужный вариант из списка\n',
                        parse_mode=types.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())


def register_dp(dp):
    dp.register_message_handler(main_help, commands="help")
