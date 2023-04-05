from discord import app_commands
from discord import Color
import discord
from discord.ext import commands
import discord.ext
from settings import *

class ModerateUserUponJoin(discord.ui.View):
    def __init__(self, reason, user, interaction):
        super().__init__()
        self.value = None
        self.reason = reason
        self.user = user
        self.interaction = interaction

    @discord.ui.button(label="Kick Member", style=discord.ButtonStyle.red)
    async def banyes(self, interaction: discord.Interaction, button: discord.Button):
        await self.interaction.guild.kick(self.user, reason=self.reason)
        await interaction.followup.send(content=f"{self.user.mention} has been banned.", view=None, ephemeral=True)

    @discord.ui.button(label="Ban Member", style=discord.ButtonStyle.red)
    async def banno(self, interaction: discord.Interaction, button: discord.Button):
        await self.interaction.guild.ban(self.user, reason=self.reason)
        await interaction.followup.send(content=f"{self.user.mention} has been banned", view=None, ephemeral=True)




class memberjoin(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_join(self, user):
        channel_id = channels.get(user.guild.id)
        designated_channel = self.client.get_channel(channel_id)
        guild = user.guild
        guild_name = guild.name
        reason = "Account marked as suspicious."
        interaction = await designated_channel.send(
            f"Do you believe this account is suspicious? If so click one of the buttons below to kick or ban them from the server.", 
            view=ModerateUserUponJoin(reason, user, interaction)
        )

        embed = discord.Embed(color=discord.Color.green(), title="New Member")
        embed.description = f"> **Member Joined:** {user.mention} \n > **Guild:** {guild_name}"
        if user.avatar:
            embed.set_image(url=user.avatar.url)
        else:
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1064941475688886272/1090678492456296468/download_7.png")
        await designated_channel.send(embed=embed)
        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(memberjoin(client))