from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated, InvalidUserId
from aiogram import types
from aiogram.dispatcher import Dispatcher
import logging


async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    logger = logging.getLogger('aiogram_events')
    logger.error(f"Bot blocked by user {update.message.from_user.id}")
    return True


async def error_chat_not_found(update: types.Update, exception: ChatNotFound):
    logger = logging.getLogger('aiogram_events')
    logger.error(f"Chat {update.message.chat.id} not found")
    return True


async def error_user_deleted(update: types.Update, exception: UserDeactivated):
    logger = logging.getLogger('aiogram_events')
    logger.error(f"User {update.message.from_user.id} deactivated")
    return True


async def error_user_invalid(update: types.Update, exception: InvalidUserId):
    logger = logging.getLogger('aiogram_events')
    logger.error(f"User ID {update.message.from_user.id} is invalid")
    return True


def register_errors_handlers(dp: Dispatcher):
    dp.register_errors_handler(error_bot_blocked, exception=BotBlocked)
    dp.register_errors_handler(error_user_deleted, exception=UserDeactivated)
    dp.register_errors_handler(error_chat_not_found, exception=ChatNotFound)
    dp.register_errors_handler(error_user_invalid, exception=InvalidUserId)
