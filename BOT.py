import discord
from discord.ext import commands
from discord import Embed
from discord import app_commands
import configparser
import requests
import random

config = configparser.ConfigParser()
config.read('config.ini')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "/" , intents = intents )

GUILD_ID = config.get('CONFIG', 'GUILD_ID')


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"{synced}")
    except Exception as e:
        print(e)
        
@bot.tree.command(name="hello", description="Say hello !")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Bonjour {interaction.user.global_name}!")

    
@bot.tree.command(name="delete", description="Delete some messages")
@app_commands.guilds(discord.Object(id=GUILD_ID))
@app_commands.describe(number="Number of message you want to delete")
async def delete(interaction: discord.Interaction, number: int ):
    messages = [message async for message in interaction.channel.history(limit=number + 1)]
    for msg in messages:
      await msg.delete()
      
    notif = Embed(color=0x77b255)
    notif.add_field(name="✅ {nb} messages deleted succesfully !".format(nb = number), value="")
    await interaction.response.send_message(embed=notif)
    
@bot.tree.command(name="dog", description="Send random picture of dog")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def dog(interaction: discord.Interaction):
    request = requests.get("https://dog.ceo/api/breeds/image/random")
    response = request.json()
    await interaction.response.send_message(response['message'])

    
@bot.tree.command(name="duck", description="Send random picture of duck")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def duck(interaction: discord.Interaction):
    request = requests.get("https://random-d.uk/api/random")
    response = request.json()
    await interaction.response.send_message(response['url'])
    
@bot.tree.command(name="fox", description="Send random picture of fox")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def fox(interaction: discord.Interaction):
    request = requests.get("https://randomfox.ca/floof")
    response = request.json()
    await interaction.response.send_message(response['image'])
    
@bot.tree.command(name="random", description="Give random number between min and max")
@app_commands.guilds(discord.Object(id=GUILD_ID))
@app_commands.describe(min="Min number", max="Max number")
async def randomNumber(interaction: discord.Interaction, min: int, max: int):
    randomNumber = random.randint(min, max)
    notif = Embed(color=0x77b255)
    notif.add_field(name="🎲 Nombre aléatoire entre {minimum} et {maximum} : {resultat}".format(minimum = min, maximum = max, resultat = randomNumber), value="")
    await interaction.response.send_message(embed=notif)
    
bot.run(token=config.get('CONFIG', 'TOKEN'))