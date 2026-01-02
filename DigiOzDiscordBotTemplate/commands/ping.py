import discord
from discord.ext import commands

@commands.command(name='ping')
async def ping(ctx):
    """Simple command to check bot responsiveness and latency."""
    latency_ms = round(ctx.bot.latency * 1000)
    await ctx.send(f"Pong! Latency: {latency_ms}ms")


async def setup(bot):
    bot.add_command(ping)


# Slash command registration for app commands
@discord.app_commands.command(name='ping', description='Check bot latency')
async def ping_slash(interaction: discord.Interaction):
    latency_ms = round(interaction.client.latency * 1000)
    await interaction.response.send_message(f"Pong! Latency: {latency_ms}ms")

async def setup_app_commands(bot):
    bot.tree.add_command(ping_slash)
