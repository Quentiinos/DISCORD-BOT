import discord
from discord.ext import commands
from discord import Embed, app_commands

class Delete(commands.Cog):
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id

    # --------------------------------------------------------------------------- LOADING COMMANDS INTO SLASH TREE
    async def cog_load(self):
        self.bot.tree.add_command(
            app_commands.Command(
                name="delete",
                description="Delete some messages",
                callback=self.delete
            ),
            guild=discord.Object(id=self.guild_id)
        )
    # --------------------------------------------------------------------------- DELETE COMMAND
    @app_commands.describe(number="Number of messages you want to delete")
    async def delete(self, interaction: discord.Interaction, number: int):
        messages = [message async for message in interaction.channel.history(limit=number)]
        for msg in messages:
            await msg.delete()

        notif = Embed(color=0x77b255)
        notif.add_field(name=f"✅ {number} messages deleted successfully!", value="")
        await interaction.response.send_message(embed=notif)


async def setup(bot):
    guild_id = bot.guild_id
    await bot.add_cog(Delete(bot, guild_id))
