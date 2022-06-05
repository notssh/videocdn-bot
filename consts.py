from typing import List, Optional

# [Bot Settings]
bot_token: str = 'your_telegram_bot_token'
owners_ids: List[int] = []  # Insert your ID there?
restrict_mode: bool = False
dispatcher_skip_updates: bool = True

# [VideoCDN API Settings]
videocdn_token: str = 'your_videocdn_token'
videocdn_custom_settings: bool = False
# if videocdn_custom_settings == True, these parameters would be used
videocdn_proxy_list: List[str] = []  # any aiohttp compatible proxies (HTTP and some HTTPS). When requesting the API, a random one will be selected from this list
videocdn_client_headers: dict = {}  # Do not specify access_token there, it's always added automatically as GET parameter
videocdn_api_server: str = 'https://videocdn.tv/api'

# [Analytics Database]
database_url: Optional[str] = None  # DB will not be used, analytics will not be collected
# database_url: Optional[str] = "sqlite+aiosqlite:///./db/analytics.db"  # DB will be used, analytics will be collected.
# Use with any asynchronous connector compatible with SQLAlchemy (for example, aiosqlite (SQLite), asyncpg (PSQL))

# [Log Settings]
logs_enabled: bool = True
logs_dir: str = './logs'
logs_rotating_size: int = 1048576
logs_backup_count: int = 5

# [Updates]
check_updates: bool = True
bot_version: str = 'v1'  # Don't edit this
