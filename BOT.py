import discord
from discord.ext import commands
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = "!" , intents = intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# @bot.event
# async def on_message(message):
#   if message.author == bot.user:
#     return
#   elif message.content.startswith('!bonjour'):
#     await message.channel.send('Bonjour !')
    
#   await bot.process_commands(message)
    
@bot.command()
async def hello(ctx):
    await ctx.send("Bonjour " + ctx.author.global_name + " !")
    
@bot.command()
async def deleteMsgs(channel: discord.TextChannel, nbMsgs: int = commands.parameter(default=1, description="Number of messages you want to delete")):
    messages = [message async for message in channel.history(limit=nbMsgs + 1)]
    for msg in messages:
      await msg.delete()

bot.run(token=config.get('CONFIG', 'TOKEN'))