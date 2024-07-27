import discord
from discord.ext import commands
from discord import app_commands
import requests

class Animals(commands.Cog):
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.command_dog = app_commands.Command(
            name="dog",
            description="Send random picture of dog",
            callback=self.dog
        )
        self.command_dog.guild_only = True

        self.command_duck = app_commands.Command(
            name="duck",
            description="Send random picture of duck",
            callback=self.duck
        )
        self.command_duck.guild_only = True

        self.command_fox = app_commands.Command(
            name="fox",
            description="Send random picture of fox",
            callback=self.fox
        )
        self.command_fox.guild_only = True

    async def cog_load(self):
        self.bot.tree.add_command(
            self.command_dog,
            guild=discord.Object(id=self.guild_id)
        )
        self.bot.tree.add_command(
            self.command_duck,
            guild=discord.Object(id=self.guild_id)
        )
        self.bot.tree.add_command(
            self.command_fox,
            guild=discord.Object(id=self.guild_id)
        )

    async def dog(self, interaction: discord.Interaction):
        response = requests.get("https://dog.ceo/api/breeds/image/random").json()
        await interaction.response.send_message(response['message'])
    
    async def duck(self, interaction: discord.Interaction):
        response = requests.get("https://random-d.uk/api/random").json()
        await interaction.response.send_message(response['url'])

    async def fox(self, interaction: discord.Interaction):
        response = requests.get("https://randomfox.ca/floof").json()
        await interaction.response.send_message(response['image'])

async def setup(bot):
    guild_id = bot.guild_id
    await bot.add_cog(Animals(bot, guild_id))
