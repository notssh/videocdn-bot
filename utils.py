from aiogram.utils import markdown as md
import aiohttp


def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def format_links_html(data):
    media = []
    if data.imdb_id:
        media.append(md.hlink('[IMDB]', f'https://www.imdb.com/title/{data.imdb_id}/'))
    if data.kinopoisk_id:
        media.append(md.hlink('[Кинопоиск]', f'https://www.kinopoisk.ru/series/{data.kinopoisk_id}/'))
    if data.worldart_id:
        media.append(md.hlink('[WorldArt]', f'http://www.world-art.ru/animation/animation.php?id={data.worldart_id}/'))
    return ' '.join(media)


# async def latest_release_on_github():
#     async with aiohttp.ClientSession() as session:
#         async with session.get(f'https://api.github.com/repos/notssh/videocdn-bot/releases/latest') as response:
#             if response.status == 200:
#                 return (await response.json())['name']
#             else:
#                 raise Exception(response.status, await response.text())
