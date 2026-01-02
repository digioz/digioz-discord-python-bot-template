import os
import importlib
import pkgutil
import asyncio
import discord
from config import TOKEN, DB_CONFIG, MESSAGE_CONTENT_INTENT, GUILD_ID
from bot_core import BotClient

# validate token
TOKEN = TOKEN.strip() if isinstance(TOKEN, str) else TOKEN
if not TOKEN or TOKEN == 'YOUR_DISCORD_APP_TOKEN':
    raise RuntimeError("Discord bot token is not set. Set the DISCORD_TOKEN environment variable or update config.py with a valid token.")

bot = BotClient(token=TOKEN, db_config=DB_CONFIG, message_content_intent=MESSAGE_CONTENT_INTENT, guild_id=GUILD_ID)

# Remove default help
bot.remove_command('help')

# No import-time scheduling here; BotClient.setup_hook loads command modules async.
# If you want to keep synchronous-only setup calls:
package = 'commands'
package_path = os.path.join(os.path.dirname(__file__), package)
for finder, name, ispkg in pkgutil.iter_modules([package_path]):
    module = importlib.import_module(f'{package}.{name}')
    setup = getattr(module, 'setup', None)
    if setup is not None and not asyncio.iscoroutinefunction(setup):
        setup(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_guild_join(guild):
    try:
        await bot.tree.sync(guild=discord.Object(id=guild.id))
        print(f'Synced commands to guild {guild.id}')
    except Exception as exc:
        print(f'Failed to sync commands to guild {guild.id}: {exc}')

if __name__ == '__main__':
    bot.run_bot()