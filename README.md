# DigiOz Discord Python Bot Template

A minimal starter template for building Discord bots in Python using `discord.py` (v2+) with async MySQL persistence and support for both prefix and slash (application) commands.

Features
- `discord.py` v2+ ready (application commands / slash commands)
- Asynchronous MySQL connection pooling via `aiomysql`
- Automatic command module loading from `commands/`
- Example prefix and slash commands (`ping`, `profile`)
- Optional Message Content intent support
- `.env` configuration support via `python-dotenv`

Requirements
- Python 3.8+
- MySQL or compatible server for the included example database usage

Quickstart
1. Create a virtual environment and install dependencies:

   python -m venv .venv
   .venv\Scripts\activate  (Windows) or source .venv/bin/activate (macOS/Linux)
   pip install -r DigiOzDiscordBotTemplate/requirements.txt

2. Copy and edit the `.env` file in `DigiOzDiscordBotTemplate/.env` and set a valid `DISCORD_TOKEN`. Do NOT commit secrets to source control.

3. Adjust database settings in the `.env` (or `config.py`) if you want to use the example MySQL-backed profile system.

4. Run the bot:

   python DigiOzDiscordBotTemplate/bot.py

Configuration
- `DISCORD_TOKEN` — Your bot token (required).
- `MESSAGE_CONTENT_INTENT` — `true`/`false` to request the privileged message content intent.
- `GUILD_ID` — Optional numeric guild ID for faster slash command registration during development.
- `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` — MySQL connection settings used by `aiomysql`.

Project Structure
- `DigiOzDiscordBotTemplate/`
  - `bot.py` — Entry point that creates and runs the `BotClient`.
  - `bot_core.py` — `BotClient` subclass that handles DB pool, loading command modules, and syncing app commands.
  - `config.py` — Loads environment variables and exposes settings.
  - `commands/` — Directory for command modules (prefix and app command setup functions supported).
  - `.env` — Example environment file (do not commit real tokens)
  - `requirements.txt` — Python dependencies

Example Commands
- `!ping` and `/ping` — Returns latency.
- `!profile` and `/profile` — Shows or creates a simple user profile stored in MySQL (credits).

Notes
- The template automatically creates a `users` table on startup if it does not exist.
- If you enable `MESSAGE_CONTENT_INTENT`, make sure your bot has the intent enabled in the Discord Developer Portal and your bot is verified if needed.

Contributing
Contributions and issues are welcome. Please follow standard GitHub workflow: fork, branch, PR.

License
This template does not include a license file by default. Add a `LICENSE` to specify usage terms.
