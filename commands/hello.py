import discord
from discord.ext import commands
from discord import app_commands

class Hello(commands.Cog):
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id


    # --------------------------------------------------------------------------- LOADING COMMANDS INTO SLASH TREE
    async def cog_load(self):
        self.bot.tree.add_command(
            app_commands.Command(
                name="hello",
                description="Say hello !",
                callback=self.hello
            ),
            guild=discord.Object(id=self.guild_id)
        )
        self.bot.tree.add_command(
            app_commands.Command(
                name="say",
                description="Something the bot would like to say",
                callback=self.say
            ),
            guild=discord.Object(id=self.guild_id)
        )
    # --------------------------------------------------------------------------- HELLO COMMAND
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Bonjour {interaction.user.global_name} !")

    # --------------------------------------------------------------------------- SAY COMMAND
    @app_commands.describe(message="The text that the bot will say")
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

async def setup(bot):
    guild_id = bot.guild_id
    await bot.add_cog(Hello(bot, guild_id))
