# OSAC Music Bot For Discord

This is a music bot that play youtube songs and more (with url) on discord. Primarily made for running in OSAC server.

This project is made with python and its discord.py library.

> To learn how to make a discord bot in python, follow this great tutorial, [link here](https://realpython.com/how-to-make-a-discord-bot-python/)

## Installation instruction
Install [python](https://python.org/downloads) and [poetry](https://python-poetry.org/docs/#installation)

Clone this repository and cd into it

Then do,
```bash
poetry install
poetry run python main.py
```

Or if you want to install with Pip (without poetry)

```bash
python -m pip install -r requirements.txt
python main.py
```

You will need to setup discord bot on developers portal of discord then export `OWNER_ID` and `DISCORD_TOKEN` environment variable to your discord id and bot's token respectively.
Use this tutorial to learn more about it

https://realpython.com/how-to-make-a-discord-bot-python/
