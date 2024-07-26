import discord
from discord.ext import commands
from discord import app_commands
import requests

class Duck(commands.Cog):
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.command_duck = app_commands.Command(
            name="duck",
            description="Send random picture of duck",
            callback=self.duck
        )
        self.command_duck.guild_only = True

    async def cog_load(self):
        self.bot.tree.add_command(
            self.command_duck,
            guild=discord.Object(id=self.guild_id)
        )

    async def duck(self, interaction: discord.Interaction):
        response = requests.get("https://random-d.uk/api/random").json()
        await interaction.response.send_message(response['url'])

async def setup(bot):
    guild_id = bot.guild_id
    await bot.add_cog(Duck(bot, guild_id))
