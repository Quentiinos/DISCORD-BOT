import discord
from discord.ext import commands
from discord import Embed
import configparser
import requests
import random

config = configparser.ConfigParser()
config.read('config.ini')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = "!" , intents = intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    
@bot.command()
async def hello(context):
    await context.send("Bonjour " + context.author.global_name + " !")
    
@bot.command()
async def delete(channel: discord.TextChannel, nbMsgs: int = commands.parameter(default=1, description="Number of messages you want to delete")):
    messages = [message async for message in channel.history(limit=nbMsgs + 1)]
    for msg in messages:
      await msg.delete()
      
    notif = Embed(color=0x77b255)
    notif.add_field(name="✅ {nb} messages deleted succesfully !".format(nb = nbMsgs), value="")
    await channel.send(embed=notif)
    
@bot.command()
async def dog(context):
    request = requests.get("https://dog.ceo/api/breeds/image/random")
    response = request.json()
    await context.send(response['message'])
    
@bot.command()
async def duck(context):
    request = requests.get("https://random-d.uk/api/random")
    response = request.json()
    await context.send(response['url'])
    
@bot.command()
async def fox(context):
    request = requests.get("https://randomfox.ca/floof")
    response = request.json()
    await context.send(response['image'])
    
@bot.command()
async def randomNumber(context, min: int = commands.parameter(default=1, description="Min value to choose random"), max: int = commands.parameter(default=2, description="Max value to choose random")):
    randomNumber = random.randint(min, max)
    notif = Embed(color=0x77b255)
    notif.add_field(name="🎲 Nombre aléatoire entre {minimum} et {maximum} : {resultat}".format(minimum = min, maximum = max, resultat = randomNumber), value="")
    await context.send(embed=notif)

bot.run(token=config.get('CONFIG', 'TOKEN'))