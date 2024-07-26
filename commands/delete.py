import discord
from discord.ext import commands
from discord import Embed, app_commands

class Delete(commands.Cog):
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.command_delete = app_commands.Command(
            name="delete",
            description="Delete some messages",
            callback=self.delete
        )
        self.command_delete.guild_only = True

    async def cog_load(self):
        self.bot.tree.add_command(
            self.command_delete,
            guild=discord.Object(id=self.guild_id)
        )

    @app_commands.describe(number="Number of messages you want to delete")
    async def delete(self, interaction: discord.Interaction, number: int):
        messages = [message async for message in interaction.channel.history(limit=number)]
        for msg in messages:
            await msg.delete()

        notif = Embed(color=0x77b255)
        notif.add_field(name="✅ {nb} messages deleted successfully!".format(nb=number), value="")
        await interaction.response.send_message(embed=notif)

async def setup(bot):
    guild_id = bot.guild_id
    await bot.add_cog(Delete(bot, guild_id))
