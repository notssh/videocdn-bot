import utils
import consts
import videocdn_api
from videocdn_api.exceptions import ApiFailedException
import log
from aiogram import types
from aiogram.utils import markdown as md
from aiogram.dispatcher import Dispatcher

if consts.videocdn_custom_settings:
    vcdn_api = videocdn_api.Api(consts.videocdn_token,
                                consts.videocdn_proxy_list,
                                consts.videocdn_client_headers,
                                consts.videocdn_api_server)
else:
    vcdn_api = videocdn_api.Api(consts.videocdn_token)
logger = log.get_inline_mode_logger()


async def inline_handler(query: types.InlineQuery):
    if consts.restrict_mode and query.from_user.id not in consts.owners_ids:
        return await query.answer(
            [types.InlineQueryResultArticle(
                id='temp_restricted', title=f'Бот временно недоступен',
                input_message_content=types.InputTextMessageContent("Бот временно недоступен"))])
    if consts.database_url is not None:
        from database import update_user_usage_count
        await update_user_usage_count(query.from_user.id, 'inline')
    logger.info(f'[{query.from_user.id}] {query.query}')
    if not query.query:
        return await query.answer(
            [types.InlineQueryResultArticle(
                id='api_fail500', title=f'Введите название',
                input_message_content=types.InputTextMessageContent("Введите название"))])
    try:
        response = await vcdn_api.short.get(title=query.query)
    except ApiFailedException as code:
        return await query.answer(
            [types.InlineQueryResultArticle(
                id='api_fail500', title=f'Ошибка на стороне сервера VideoCDN.tv (код {code})',
                input_message_content=types.InputTextMessageContent(
                    f"Ошибка на стороне сервера VideoCDN.tv (код {code})"))])
    except Exception as e:
        await query.answer(
            [types.InlineQueryResultArticle(
                id='fail1', title=f'Что-то пошло не так',
                input_message_content=types.InputTextMessageContent("Что-то пошло не так"))])
        raise e
    if not response.data:
        return await query.answer(
            [types.InlineQueryResultArticle(
                id='not_found', title=f'Нет результатов',
                input_message_content=types.InputTextMessageContent('*Нет результатов*',
                                                                    parse_mode=types.ParseMode.MARKDOWN))])
    articles = []
    for item in response.data:
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
                           f'Обновлен: {item.update}\n' \
                           f'{md.hlink("[Смотреть на VideoCDN]", f"https:{item.iframe_src}")}\n\n'
        else:
            message_text = f'<b>{(md.quote_html(item.title))}</b>\n' \
                           f'{utils.format_links_html(item)}\n\n' \
                           f'Оригинальное название: {md.quote_html(item.orig_title)}\n' \
                           f'Тип: {md.quote_html(item.type)}\n' \
                           f'Год: {item.year}\n' \
                           f'Качество: {md.quote_html(item.quality) if item.quality else "неизвестно"}\n' \
                           f'Озвучка: {translations}\n' \
                           f'Добавлен: {item.add}\n' \
                           f'Обновлен: {item.update}\n' \
                           f'{md.hlink("[Смотреть на VideoCDN]", f"https:{item.iframe_src}")}\n\n'
        # keyboard = types.InlineKeyboardMarkup(row_width=1)
        # keyboard.add(types.InlineKeyboardButton(
        #     text="Смотреть на VideoCDN",
        #     url=f"https:{item.iframe_src}"))
        # Нельзя так с инлайном, увы
        articles.append(types.InlineQueryResultArticle(
            id=item.id,
            title=f'{item.title} ({item.year.year})',
            description=item.type.capitalize(),
            hide_url=False,
            input_message_content=types.InputTextMessageContent(
                message_text=message_text,
                parse_mode=types.ParseMode.HTML, disable_web_page_preview=True,
            )))
    await query.answer(articles, cache_time=60, is_personal=True)


def register_dp(dp: Dispatcher):
    dp.register_inline_handler(inline_handler, run_task=True)
