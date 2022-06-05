from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import func
import consts
import middleware
import log
import error_handlers
# import utils
import videocdn_api
from videocdn_api.exceptions import ApiFailedException, ApiTokenInvalid
from aiogram.utils.exceptions import Unauthorized

logger = log.get_main_logger()


async def set_commands(bot: Bot):
    bot_commands = [
        BotCommand(command="/search", description="Быстрый поиск"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/about", description="О проекте")
    ]
    await bot.set_my_commands(bot_commands)


async def main():
    # if consts.check_updates is True:
    #     try:
    #         github_latest_ver = await utils.latest_release_on_github()
    #         if github_latest_ver != consts.bot_version:
    #             logger.warning(f"Update available! Current version: {consts.bot_version}, latest: {github_latest_ver}")
    #             logger.warning(f"https://github.com/notssh/videocdn-bot/")
    #     except:
    #         logger.warning(f"Failed to check for updates")
    try:
        bot = Bot(token=consts.bot_token)
        bot_info = await bot.get_me()
    except Unauthorized as exception:
        logger.error("Unable to connect to the bot. Is the correct token specified?")
        raise exception
    dp = Dispatcher(bot, storage=MemoryStorage())
    logger.warning(f"Starting bot \"{bot_info.full_name}\" [ID{bot.id}]")
    if consts.database_url is not None:
        import database
        logger.warning("The database is specified, analytics will be collected")
        logger.warning("Creating tables in DB if required...")
        await database.setup_db_if_required()
    else:
        logger.warning("The database is not specified, analytics will not be collected")
    if consts.videocdn_token:
        try:
            if consts.videocdn_custom_settings:
                await videocdn_api.Api(consts.videocdn_token,
                                       consts.videocdn_proxy_list,
                                       consts.videocdn_client_headers,
                                       consts.videocdn_api_server).short.get(limit=1)
            else:
                await videocdn_api.Api(consts.videocdn_token).short.get(limit=1)
            logger.warning(f"VideoCDN API works!")
        except ApiFailedException as exception:
            logger.error(f"VideoCDN API failed (HTTP {exception})! Exiting...")
            raise exception
        except ApiTokenInvalid as exception:
            logger.error(f"Invalid VideoCDN token specified! Exiting...")
            raise exception
        except Exception as exception:
            logger.error(f"Something went wrong! Exiting...")
            raise exception
    else:
        logger.error(f"VideoCDN token not specified! Exiting...")
        raise ApiTokenInvalid

    logger.warning("Setup handlers and middlewares...")
    middleware.setup_middlewares(dp)
    func.register_dispatchers(dp)
    error_handlers.register_errors_handlers(dp)

    logger.warning("Setup commands...")
    await set_commands(bot)

    if consts.dispatcher_skip_updates is True:
        await dp.skip_updates()
    if consts.restrict_mode is True:
        logger.warning(f"restrict_mode is enabled! The bot is only available to users specified in owners_ids!")
    logger.warning(f"Bot \"{bot_info.full_name}\" [ID{bot.id}] is running")
    await dp.start_polling()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
