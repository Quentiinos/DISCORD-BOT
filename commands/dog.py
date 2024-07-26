import discord
from discord.ext import commands
from discord import app_commands
import requests

class Dog(commands.Cog):
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.command_dog = app_commands.Command(
            name="dog",
            description="Send random picture of dog",
            callback=self.dog
        )
        self.command_dog.guild_only = True

    async def cog_load(self):
        self.bot.tree.add_command(
            self.command_dog,
            guild=discord.Object(id=self.guild_id)
        )

    async def dog(self, interaction: discord.Interaction):
        response = requests.get("https://dog.ceo/api/breeds/image/random").json()
        await interaction.response.send_message(response['message'])

async def setup(bot):
    guild_id = bot.guild_id
    await bot.add_cog(Dog(bot, guild_id))
