import asyncio
import importlib
import os
import pkgutil
import logging
from typing import Optional

import aiomysql
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class BotClient(commands.Bot):
    def __init__(
        self,
        token: str,
        db_config: dict,
        message_content_intent: bool = False,
        guild_id: Optional[int] = None,
        commands_package: str = "commands",
        **kwargs,
    ):
        intents = discord.Intents.default()
        intents.message_content = message_content_intent
        super().__init__(command_prefix="!", intents=intents, **kwargs)
        self.db_pool: Optional[aiomysql.Pool] = None
        self._token = token
        self._db_config = db_config
        self._guild_id = guild_id
        self._commands_package = commands_package

    async def setup_hook(self) -> None:
        # Database pool creation with basic retry/backoff
        retries = 3
        delay = 1.0
        for attempt in range(1, retries + 1):
            try:
                # set sensible defaults for pool size if not provided
                pool_kwargs = dict(self._db_config)
                pool_kwargs.setdefault("minsize", 1)
                pool_kwargs.setdefault("maxsize", 10)
                self.db_pool = await aiomysql.create_pool(**pool_kwargs)
                break
            except Exception as exc:
                if attempt == retries:
                    logger.exception(
                        "Failed to create DB pool after %d attempts: %s", retries, exc
                    )
                    raise
                logger.warning(
                    "Failed to create DB pool (attempt %d/%d): %s", attempt, retries, exc
                )
                await asyncio.sleep(delay)
                delay *= 2

        # initialize table (consider migrating instead)
        try:
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
        except Exception:
            logger.exception("Failed to initialize DB schema")
            raise

        # Load command modules from the commands package
        package = self._commands_package
        package_path = os.path.join(os.path.dirname(__file__), package)
        if os.path.isdir(package_path):
            for finder, name, ispkg in pkgutil.iter_modules([package_path]):
                module_name = f"{package}.{name}"
                try:
                    module = importlib.import_module(module_name)
                except Exception:
                    logger.exception("Failed to import module %s", module_name)
                    continue

                # register prefix command setups
                setup = getattr(module, "setup", None)
                if setup is not None:
                    try:
                        if asyncio.iscoroutinefunction(setup):
                            await setup(self)
                        else:
                            setup(self)
                    except Exception:
                        logger.exception("Error running setup for %s", module_name)

                # register app command setups
                setup_app = getattr(module, "setup_app_commands", None)
                if setup_app is not None:
                    try:
                        if asyncio.iscoroutinefunction(setup_app):
                            await setup_app(self)
                        else:
                            setup_app(self)
                    except Exception:
                        logger.exception("Error running setup_app_commands for %s", module_name)

        # sync application commands
        try:
            if self._guild_id:
                guild_obj = discord.Object(id=self._guild_id)
                await self.tree.sync(guild=guild_obj)
            else:
                await self.tree.sync()
        except Exception:
            logger.exception("Failed to sync application commands")

    async def close(self) -> None:
        await super().close()
        if self.db_pool:
            try:
                self.db_pool.close()
                await self.db_pool.wait_closed()
            except Exception:
                logger.exception("Error closing DB pool")

    def run_bot(self) -> None:
        super().run(self._token)
