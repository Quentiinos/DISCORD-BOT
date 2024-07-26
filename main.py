import discord
from discord.ext import commands
import configparser
import asyncio

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config.get('CONFIG', 'TOKEN')
GUILD_ID = config.get('CONFIG', 'GUILD_ID')

intents = discord.Intents.all()

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.guild_id = GUILD_ID

bot = MyBot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=bot.guild_id))
        print(f"{synced}")
    except Exception as e:
        print(e)

async def load_extensions():
    for extension in ["commands.hello", "commands.delete", "commands.dog", "commands.duck", "commands.fox", "commands.random",]:
        await bot.load_extension(extension)

async def main():
    await load_extensions()
    await bot.start(TOKEN)

asyncio.run(main())
