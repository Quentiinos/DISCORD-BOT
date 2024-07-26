import discord
from discord.ext import commands
from discord import app_commands

class Hello(commands.Cog):
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id

    async def cog_load(self):
        self.bot.tree.add_command(
            app_commands.Command(
                name="hello",
                description="Say hello!",
                callback=self.hello
            ),
            guild=discord.Object(id=self.guild_id)
        )

    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Bonjour {interaction.user.global_name}!")

async def setup(bot):
    guild_id = bot.guild_id
    await bot.add_cog(Hello(bot, guild_id))
