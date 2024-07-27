import discord
from discord.ext import commands
from discord import Embed, app_commands
import random

class Random(commands.Cog):
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id

    # --------------------------------------------------------------------------- LOADING COMMANDS INTO SLASH TREE
    async def cog_load(self):
        self.bot.tree.add_command(
            app_commands.Command(
                name="random",
                description="Give random number between min and max",
                callback=self.random_number
            ),
            guild=discord.Object(id=self.guild_id)
        )

    # --------------------------------------------------------------------------- RANDOM COMMAND
    @app_commands.describe(min="Min number", max="Max number")
    async def random_number(self, interaction: discord.Interaction, min: int, max: int):
        random_number = random.randint(min, max)
        notif = Embed(color=0x77b255)
        notif.add_field(name=f"🎲 Nombre aléatoire entre {min} et {max} : {random_number}", value="")
        await interaction.response.send_message(embed=notif)

        

async def setup(bot):
    guild_id = bot.guild_id
    await bot.add_cog(Random(bot, guild_id))
