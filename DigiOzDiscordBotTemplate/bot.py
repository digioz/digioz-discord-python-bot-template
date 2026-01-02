import logging
import os
import discord

from config import TOKEN, DB_CONFIG, MESSAGE_CONTENT_INTENT, GUILD_ID
from bot_core import BotClient

# Configure basic logging for the service
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# validate token
TOKEN = TOKEN.strip() if isinstance(TOKEN, str) else TOKEN
if not TOKEN:
    raise RuntimeError("Discord bot token is not set. Set the DISCORD_TOKEN environment variable.")

bot = BotClient(
    token=TOKEN,
    db_config=DB_CONFIG,
    message_content_intent=MESSAGE_CONTENT_INTENT,
    guild_id=GUILD_ID,
)

# Remove default help
try:
    bot.remove_command("help")
except Exception:
    logger.debug("Default help command not present or already removed")

# NOTE: Do not import or register commands synchronously here.
# BotClient.setup_hook will load commands asynchronously. This avoids duplicate imports.

@bot.event
async def on_ready():
    logger.info("Logged in as %s (ID: %s)", bot.user, bot.user.id)
    logger.info("------")

@bot.event
async def on_guild_join(guild):
    try:
        await bot.tree.sync(guild=discord.Object(id=guild.id))
        logger.info("Synced commands to guild %s", guild.id)
    except Exception:
        logger.exception("Failed to sync commands to guild %s", guild.id)

if __name__ == "__main__":
    bot.run_bot()