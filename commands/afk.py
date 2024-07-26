import discord
from discord.ext import commands
from discord import app_commands

class AFK(commands.Cog):
    def __init__(self, bot, guild_id, afk_channel_id):
        self.bot = bot
        self.guild_id = guild_id
        self.afk_channel_id = afk_channel_id

    async def cog_load(self):
        self.bot.tree.add_command(
            app_commands.Command(
                name="afk",
                description="Move yourself to the AFK voice channel",
                callback=self.afk
            ),
            guild=discord.Object(id=self.guild_id)
        )

    async def afk(self, interaction: discord.Interaction):
        guild = discord.utils.get(self.bot.guilds, id=self.guild_id)
        afk_channel = guild.get_channel(self.afk_channel_id)

        if not afk_channel or not isinstance(afk_channel, discord.VoiceChannel):
            await interaction.response.send_message("AFK voice channel is not properly configured.")
            return

        member = interaction.user
        if member.voice:
            try:
                # Move the user to the AFK voice channel
                await member.move_to(afk_channel, reason="User went AFK")
                                
                await interaction.response.send_message("You have been moved to the AFK channel.")
            except discord.Forbidden:
                await interaction.response.send_message("I don't have permission to move you.")
        else:
            await interaction.response.send_message("You are not in a voice channel.")

async def setup(bot):
    guild_id = bot.guild_id
    afk_channel_id = bot.afk_channel_id
    await bot.add_cog(AFK(bot, guild_id, afk_channel_id))
