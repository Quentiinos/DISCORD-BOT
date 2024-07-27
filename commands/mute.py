import discord
from discord.ext import commands
from discord import Embed, app_commands
import asyncio

class Mute(commands.Cog):
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id

    # --------------------------------------------------------------------------- LOADING COMMANDS INTO SLASH TREE
    async def cog_load(self):
        self.bot.tree.add_command(
            app_commands.Command(
                name="mute",
                description="Mute a user for a specified duration",
                callback=self.mute_user
            ),
            guild=discord.Object(id=self.guild_id)
        )
        self.bot.tree.add_command(
            app_commands.Command(
                name="unmute",
                description="Unmute a user",
                callback=self.unmute_user
            ),
            guild=discord.Object(id=self.guild_id)
        )

    # --------------------------------------------------------------------------- MUTE COMMAND
    @app_commands.describe(user="User you want to mute", duration="Mute duration in seconds", reason="The reason why this user is muted")
    async def mute_user(self, interaction: discord.Interaction, user: discord.Member, duration: int, reason: str = "No reason provided"):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not role:
            role = await interaction.guild.create_role(
                name="Muted",
                reason="Role created for muting users",
                hoist=False,
                mentionable=False
            )
            # Ensure the role is hidden and doesn't display separately
            await role.edit(hoist=False, mentionable=False)

            for channel in interaction.guild.channels:
                if isinstance(channel, discord.TextChannel):
                    await channel.set_permissions(role, send_messages=False, read_message_history=True, read_messages=False)
                elif isinstance(channel, discord.VoiceChannel):
                    await channel.set_permissions(role, speak=False, connect=False)

        await user.add_roles(role, reason=reason)
        
        muted = Embed(color=0xff0000)
        muted.add_field(
            name=f"🔇 {user.name} has been muted !",
            value=f"Duration: {duration} minutes\nReason: {reason}"
        )
        await interaction.response.send_message(embed=muted, ephemeral=True)

        await asyncio.sleep(duration * 60)
        
        await user.remove_roles(role, reason="Mute duration expired")

        unmuted = Embed(color=0x77b255)
        unmuted.add_field(
            name=f"🔊 {user.name} has been unmuted !",
            value="Mute duration expired"
        )
        await interaction.followup.send(embed=unmuted, ephemeral=True)




    # --------------------------------------------------------------------------- UNMUTE COMMAND
    @app_commands.describe(user="User you want to unmute")
    async def unmute_user(self, interaction: discord.Interaction, user: discord.Member):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        if role in user.roles:
            await user.remove_roles(role, reason="Unmuted by command")
            
            unmuted = Embed(color=0x77b255)
            unmuted.add_field(
                name=f"🔊 {user.name} has been unmuted !",
                value=""
            )
            await interaction.response.send_message(embed=unmuted, ephemeral=True)
        else:
            await interaction.response.send_message(content=f"{user.name} is not muted.", ephemeral=True)





async def setup(bot):
    guild_id = bot.guild_id
    await bot.add_cog(Mute(bot, guild_id))
