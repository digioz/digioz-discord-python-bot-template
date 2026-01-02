import os
from dotenv import load_dotenv

# Load environment variables from a .env file when available
load_dotenv()

# Discord token must be provided via environment variable
TOKEN = os.getenv('DISCORD_TOKEN')

# Whether to request the privileged message content intent. Set to 'true'/'1' to enable.
MESSAGE_CONTENT_INTENT = os.getenv('MESSAGE_CONTENT_INTENT', 'false').lower() in ('1', 'true', 'yes')

# Optional guild ID for faster slash command registration during development
# Read from the GUILD_ID environment variable and convert to int when present
_GUILD_ID = os.getenv('GUILD_ID')
try:
    GUILD_ID = int(_GUILD_ID) if _GUILD_ID is not None else None
except ValueError:
    GUILD_ID = None

# Database config
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', None),
    'db': os.getenv('DB_NAME', 'discord_bot_db_1'),
    'autocommit': True
}
