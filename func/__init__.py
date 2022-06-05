from aiogram.dispatcher import Dispatcher
from func import common, help, inline_search, search


def register_dispatchers(dp: Dispatcher):
    common.register_dp(dp)
    help.register_dp(dp)
    inline_search.register_dp(dp)
    search.register_dp(dp)
