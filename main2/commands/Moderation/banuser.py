import discord
from discord.ext import commands
from discord import app_commands
import traceback
from settings import *
from sqlite3 import Error


class AuthorBannedMenu(discord.ui.View):
    def __init__(self, interaction):
        super().__init__()
        self.banned_users = banned_users_dic
        self.reason = self.banned_users.get(str(interaction.user.id), None)

    @discord.ui.button(label="Reason", style=discord.ButtonStyle.red)
    async def internalbanreason(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(f"{self.reason}", ephemeral=True)
        

class UserBannedMenu(discord.ui.View):
    def __init__(self, reason, user, interaction):
        super().__init__()
        self.banned_users = banned_users_dic
        self.lol = self.banned_users.get(str(user.id), None)
        self.reason = reason
        self.value = None
        self.user = user
        self.interaction = interaction
    
    @discord.ui.button(label="X-Bot Ban Reason", style=discord.ButtonStyle.red)
    async def Moderateinternalbanreason(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(f"{self.lol}", ephemeral=True)

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def banyes(self, interaction: discord.Interaction, button: discord.Button):
        await self.interaction.guild.ban(self.user, reason=self.reason)
        await interaction.response.edit_message(content=f"{self.user.mention} has been banned.", view=None)

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def banno(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.edit_message(content="Ban canceled.", view=None)


class ApprovedMenu(discord.ui.View):
    def __init__(self, reason, user, interaction):
        super().__init__()
        self.value = None
        self.user = user
        self.reason = reason
        self.interaction = interaction

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def banyes(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.id != self.interaction.author.id:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        await self.interaction.guild.ban(self.user, reason=self.reason)
        await interaction.response.edit_message(content=f"{self.user.mention} has been banned.", view=None)

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def banno(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.id != self.interaction.author.id:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        await interaction.response.edit_message(content="Ban canceled.", view=None)


class Ban(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.hybrid_command(name="ban", description="Ban a user from a guild")
    async def ban(self, ctx, user: discord.Member, reason: str):
        mod_role_id = mod_roles.get(ctx.guild.id)
        mod_role = ctx.guild.get_role(mod_role_id)
        if mod_role in ctx.author.roles:
            if ctx.author in banned_users_dic:
                embed = discord.Embed(title="Internal Bot Ban", description=f"You appear to have been banned from xbot. You are unable to use any commands, if you believe it is false please appeal in our [support server](https://discord.gg/txMtp4ykNt)", color=discord.Color.brand_red())
                iban = AuthorBannedMenu(ctx)
                await ctx.reply(embed=embed, view=iban)


            # Ask for confirmation to ban the user
            mban = ApprovedMenu(reason, user, ctx)
            aumban = UserBannedMenu(reason, user, ctx)
            if str(user.id) in banned_users_dic:
                embed = discord.Embed(title="Internal Ban Alert", description="The user you are trying to moderate is currently banned from x-bot, please keep this in mind when communicating with them. \n \n **Are you sure you would like to ban them from this guild?**", color=discord.Color.brand_red())
                await ctx.send(f"||{user.mention}||",embed=embed, view=aumban, ephemeral=True)
            else:
                await ctx.send(f"Would you like to ban {user.mention} from this server?", view=mban, ephemeral=True)
        
        
        if mod_role_id is None:
            embed = discord.Embed(color=discord.Color.brand_red(), description=f"❌ This server has the moderation module disabled!")
            embed.set_author(name=f"{ctx.author}", url=ctx.author.avatar.url)
            await ctx(embed=embed)
        
        if mod_role not in ctx.author.roles:
            embed = discord.Embed(color=discord.Color.brand_red(), description=f"❌ This server has the moderation module disabled!")
            embed.set_author(name=f"{ctx.author}", url=ctx.author.avatar.url)
            await ctx(embed=embed)


        
    


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Ban(client))