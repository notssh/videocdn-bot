import utils
import consts
import videocdn_api
from videocdn_api.exceptions import ApiFailedException

from aiogram import types
from aiogram.utils import markdown as md
from aiogram.dispatcher import Dispatcher
from aiogram.utils.callback_data import CallbackData

if consts.videocdn_custom_settings:
    vcdn_api = videocdn_api.Api(consts.videocdn_token,
                                consts.videocdn_proxy_list,
                                consts.videocdn_client_headers,
                                consts.videocdn_api_server)
else:
    vcdn_api = videocdn_api.Api(consts.videocdn_token)

callback_search = CallbackData("search_callback", "action", "page", "query", "internal_id", "kinopoisk_id")


async def search_short(message: types.Message):
    query = message.get_args()
    if consts.database_url is not None:
        from database import update_user_usage_count
        await update_user_usage_count(message.from_user.id, 'short')
    if query:
        try:
            response = await vcdn_api.short.get(title=query, limit=10)
        except ApiFailedException as code:
            await message.reply(f'*Ошибка на стороне сервера VideoCDN.tv (код {code})*',
                                parse_mode=types.ParseMode.MARKDOWN, reply_markup=types.ReplyKeyboardRemove())
            return
        except Exception as e:
            await message.reply('*Что-то пошло не так*', parse_mode=types.ParseMode.MARKDOWN,
                                reply_markup=types.ReplyKeyboardRemove())
            raise e
        message_text = ''
        if response.data:
            buttons = []
            for item in response.data:
                message_text += f'<b>{(md.quote_html(item.title))} ({item.year.year})</b>\n' \
                                f'{md.quote_html(item.type.capitalize())}; {md.quote_html(item.orig_title)}' \
                                f'\n\n'
                buttons.append(types.InlineKeyboardButton(
                    text=f"{(md.quote_html(item.title))} ({item.year.year})",
                    callback_data=callback_search.new(
                        action="show_media",
                        page=response.current_page,
                        query=query,
                        kinopoisk_id=item.kinopoisk_id if item.kinopoisk_id else 0,
                        internal_id=item.id if item.kinopoisk_id else 0
                    )
                ))

            if response.prev_page_url:
                buttons.append(types.InlineKeyboardButton(
                    text="Предыдущая страница",
                    callback_data=callback_search.new(
                        action="switch_page",
                        page=response.current_page - 1,
                        query=query,
                        internal_id=0,
                        kinopoisk_id=0
                    )
                )
                )
            if response.next_page_url:
                buttons.append(types.InlineKeyboardButton(
                    text="Следующая страница",
                    callback_data=callback_search.new(
                        action="switch_page",
                        page=response.current_page + 1,
                        query=query,
                        kinopoisk_id=0,
                        internal_id=0
                    )
                )
                )
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            await message.reply(message_text, parse_mode=types.ParseMode.HTML,
                                reply_markup=keyboard, disable_web_page_preview=True)
        else:
            await message.reply('*Нет результатов*', parse_mode=types.ParseMode.MARKDOWN)
    else:
        await message.reply('*Укажите название или ID фильма/аниме/сериала*', parse_mode=types.ParseMode.MARKDOWN)


async def update_search_short(message: types.Message, query: str, page: int):
    try:
        response = await vcdn_api.short.get(title=query, page=page, limit=10)
    except ApiFailedException as code:
        await message.edit_text(f'*Ошибка на стороне сервера VideoCDN.tv (код {code})*',
                                parse_mode=types.ParseMode.MARKDOWN)
        return
    except Exception as e:
        await message.edit_text('*Что-то пошло не так*', parse_mode=types.ParseMode.MARKDOWN)
        raise e

    message_text = ''
    if response.data:
        buttons = []
        for item in response.data:
            message_text += f'<b>{(md.quote_html(item.title))} ({item.year.year})</b>\n' \
                            f'{md.quote_html(item.type.capitalize())}; {md.quote_html(item.orig_title)}' \
                            f'\n\n'
            buttons.append(types.InlineKeyboardButton(
                text=f"{(md.quote_html(item.title))} ({item.year.year})",
                callback_data=callback_search.new(
                    action="show_media",
                    page=response.current_page,
                    query=query,
                    kinopoisk_id=item.kinopoisk_id if item.kinopoisk_id else 0,
                    internal_id=item.id if item.kinopoisk_id else 0
                )
            ))

        if response.prev_page_url:
            buttons.append(types.InlineKeyboardButton(
                text="Предыдущая страница",
                callback_data=callback_search.new(
                    action="switch_page",
                    page=response.current_page - 1,
                    query=query,
                    kinopoisk_id=0,
                    internal_id=0
                )
            )
            )
        if response.next_page_url:
            buttons.append(types.InlineKeyboardButton(
                text="Следующая страница",
                callback_data=callback_search.new(
                    action="switch_page",
                    page=response.current_page + 1,
                    query=query,
                    kinopoisk_id=0,
                    internal_id=0
                )
            )
            )
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await message.edit_text(message_text, parse_mode=types.ParseMode.HTML,
                                reply_markup=keyboard, disable_web_page_preview=True)
    else:
        await message.edit_text('*Нет результатов*', parse_mode=types.ParseMode.MARKDOWN)


async def update_show_media(message: types.Message, internal_id: int, kinopoisk_id: int, query: str,
                            from_page: int = 1):
    try:
        if kinopoisk_id != 0:
            response = await vcdn_api.short.get(kinopoisk_id=kinopoisk_id)
        else:
            response = await vcdn_api.short.get(internal_id=internal_id)
    except ApiFailedException as code:
        return await message.edit_text(f'*Ошибка на стороне сервера VideoCDN.tv (код {code})*',
                                       parse_mode=types.ParseMode.MARKDOWN)
    except Exception as e:
        await message.edit_text('*Что-то пошло не так*', parse_mode=types.ParseMode.MARKDOWN)
        raise e
    if response.result:
        message_text = ''
        if response.data:
            buttons = []
            if response.data:
                item = response.data[0]
                if item.translations:
                    if len(item.translations) == 1:
                        translations = md.quote_html(item.translations[0])
                    else:
                        translations = md.quote_html(item.translations[0]
                                                     + f' и еще {len(item.translations) - 1} вар.')
                else:
                    translations = "отсутствует"
                if item.type == 'serial':
                    message_text = f'<b>{(md.quote_html(item.title))}</b>\n' \
                                   f'{utils.format_links_html(item)}\n\n' \
                                   f'Оригинальное название: {md.quote_html(item.orig_title)}\n' \
                                   f'Тип: {md.quote_html(item.type)}\n' \
                                   f'Сезонов: {item.seasons_count}\n' \
                                   f'Эпизодов: {item.episodes_count}\n' \
                                   f'Год: {item.year}\n' \
                                   f'Качество: {md.quote_html(item.quality) if item.quality else "неизвестно"}\n' \
                                   f'Озвучка: {translations}\n' \
                                   f'Добавлен: {item.add}\n' \
                                   f'Обновлен: {item.update}\n'
                else:
                    message_text = f'<b>{(md.quote_html(item.title))}</b>\n' \
                                   f'{utils.format_links_html(item)}\n\n' \
                                   f'Оригинальное название: {md.quote_html(item.orig_title)}\n' \
                                   f'Тип: {md.quote_html(item.type)}\n' \
                                   f'Год: {item.year}\n' \
                                   f'Качество: {md.quote_html(item.quality) if item.quality else "неизвестно"}\n' \
                                   f'Озвучка: {translations}\n' \
                                   f'Добавлен: {item.add}\n' \
                                   f'Обновлен: {item.update}\n'
                buttons.append(types.InlineKeyboardButton(
                    text="Смотреть на VideoCDN",
                    url=f"https:{item.iframe_src}"
                ))
            buttons.append(types.InlineKeyboardButton(
                text="Назад",
                callback_data=callback_search.new(
                    action="switch_page",
                    page=from_page,
                    query=query,
                    kinopoisk_id=0,
                    internal_id=0
                )
            ))
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            await message.edit_text(message_text, parse_mode=types.ParseMode.HTML,
                                    reply_markup=keyboard, disable_web_page_preview=True)
        else:
            await message.edit_text('*Нет результатов*', parse_mode=types.ParseMode.MARKDOWN)


async def callbacks_fab(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    query = callback_data["query"]
    page = callback_data["page"]
    kinopoisk_id = callback_data["kinopoisk_id"]
    internal_id = callback_data["internal_id"]
    if action == "switch_page":
        await update_search_short(call.message, query, page)
    elif action == "show_media":
        await update_show_media(call.message, internal_id, kinopoisk_id, query, page)
    await call.answer()


def register_dp(dp: Dispatcher):
    dp.register_message_handler(search_short, commands="search")
    dp.register_callback_query_handler(callbacks_fab, callback_search.filter(action=["switch_page", "show_media"]))
