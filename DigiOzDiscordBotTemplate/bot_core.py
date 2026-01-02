import discord
from discord.ext import commands
import aiomysql
import pkgutil
import importlib
import os
import asyncio

class BotClient(commands.Bot):
    def __init__(self, token, db_config, message_content_intent=False, guild_id=None, commands_package='commands', **kwargs):
        intents = discord.Intents.default()
        intents.message_content = message_content_intent
        super().__init__(command_prefix='!', intents=intents, **kwargs)
        self.db_pool = None
        self._token = token
        self._db_config = db_config
        self._guild_id = guild_id
        self._commands_package = commands_package

    async def setup_hook(self):
        # create database pool
        self.db_pool = await aiomysql.create_pool(**self._db_config)

        # initialize table
        async with self.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        discord_id BIGINT PRIMARY KEY,
                        credits INT DEFAULT 100
                    )
                    """
                )

        # Load command modules from the commands package
        package = self._commands_package
        package_path = os.path.join(os.path.dirname(__file__), package)
        if os.path.isdir(package_path):
            for finder, name, ispkg in pkgutil.iter_modules([package_path]):
                module_name = f'{package}.{name}'
                try:
                    module = importlib.import_module(module_name)
                except Exception as exc:
                    print(f'Failed to import module {module_name}: {exc}')
                    continue

                # register prefix command setups
                setup = getattr(module, 'setup', None)
                if setup is not None:
                    try:
                        if asyncio.iscoroutinefunction(setup):
                            await setup(self)
                        else:
                            setup(self)
                    except Exception as exc:
                        print(f'Error running setup for {module_name}: {exc}')

                # register app command setups
                setup_app = getattr(module, 'setup_app_commands', None)
                if setup_app is not None:
                    try:
                        if asyncio.iscoroutinefunction(setup_app):
                            await setup_app(self)
                        else:
                            setup_app(self)
                    except Exception as exc:
                        print(f'Error running setup_app_commands for {module_name}: {exc}')

        # sync application commands
        try:
            if self._guild_id:
                guild_obj = discord.Object(id=self._guild_id)
                await self.tree.sync(guild=guild_obj)
            else:
                await self.tree.sync()
        except Exception:
            print('Warning: failed to sync application commands')

    async def close(self):
        await super().close()
        if self.db_pool:
            self.db_pool.close()
            await self.db_pool.wait_closed()

    def run_bot(self):
        # wrapper to run the bot using stored token
        super().run(self._token)
