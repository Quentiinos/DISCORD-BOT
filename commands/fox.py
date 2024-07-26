import discord
from discord.ext import commands
from discord import app_commands
import requests

class Fox(commands.Cog):
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.command_fox = app_commands.Command(
            name="fox",
            description="Send random picture of fox",
            callback=self.fox
        )
        self.command_fox.guild_only = True

    async def cog_load(self):
        self.bot.tree.add_command(
            self.command_fox,
            guild=discord.Object(id=self.guild_id)
        )

    async def fox(self, interaction: discord.Interaction):
        response = requests.get("https://randomfox.ca/floof").json()
        await interaction.response.send_message(response['image'])

async def setup(bot):
    guild_id = bot.guild_id
    await bot.add_cog(Fox(bot, guild_id))
