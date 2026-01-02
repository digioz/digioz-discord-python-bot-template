import discord
from discord.ext import commands
import aiomysql

@commands.command(name='profile')
async def profile(ctx):
    """Checks the user's credits in the MySQL database."""
    user_id = ctx.author.id
    async with ctx.bot.db_pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT credits FROM users WHERE discord_id = %s", (user_id,))
            result = await cur.fetchone()
            if result:
                credits = result['credits']
                await ctx.send(f"{ctx.author.mention}, you have **{credits}** credits.")
            else:
                await cur.execute("INSERT INTO users (discord_id) VALUES (%s)", (user_id,))
                await ctx.send(f"Welcome {ctx.author.mention}! I've created a profile for you with 100 starter credits.")

async def setup(bot):
    bot.add_command(profile)

# Slash command
@discord.app_commands.command(name='profile', description='Show your credits')
async def profile_slash(interaction: discord.Interaction):
    user_id = interaction.user.id
    async with interaction.client.db_pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT credits FROM users WHERE discord_id = %s", (user_id,))
            result = await cur.fetchone()
            if result:
                credits = result['credits']
                await interaction.response.send_message(f"You have **{credits}** credits.", ephemeral=True)
            else:
                await cur.execute("INSERT INTO users (discord_id) VALUES (%s)", (user_id,))
                await interaction.response.send_message("Welcome! I've created a profile for you with 100 starter credits.", ephemeral=True)

async def setup_app_commands(bot):
    bot.tree.add_command(profile_slash)
