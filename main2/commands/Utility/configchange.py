import discord
import random
from discord import Embed, app_commands
from discord.ext import commands
import discord.ext
from settings import *


class LoggingChannelDropdown(discord.ui.Select):
    def __init__(self, guild_channels):
        options = [
            discord.SelectOption(label=f"#{channel.name}", value=str(channel.id)) for channel in guild_channels
        ]
        super().__init__(placeholder='Select a logging channel', options=options)

    async def callback(self, interaction: discord.Interaction):
        channel_id = int(self.values[0])
        channel = interaction.guild.get_channel(channel_id)
        guild_id = interaction.guild.id
        channels[guild_id] = channel.id
        c_channels.execute('INSERT OR REPLACE INTO channels (guild_id, channel_id) VALUES (?, ?)', (guild_id, channel.id))
        channel_db.commit()
        await interaction.response.send_message(f"Selected logging channel: {channel.mention}")

class LoggingChannelDropdownView(discord.ui.View):
    def __init__(self, guild_channels):
        super().__init__()
        self.add_item(LoggingChannelDropdown(guild_channels))


class ModeratorRoleDropdown(discord.ui.Select):
    def __init__(self, guild_roles):
        options = [
            discord.SelectOption(label=f"@{role.name}", value=str(role.id)) for role in guild_roles
        ]
        super().__init__(placeholder='Select a role', options=options)

    async def callback(self, interaction: discord.Interaction):
        role_id = int(self.values[0])
        role = interaction.guild.get_role(role_id)
        guild_id = interaction.guild.id
        mod_roles[guild_id] = role.id
        c_mod_roles.execute('INSERT OR REPLACE INTO mod_roles (guild_id, mod_role_id) VALUES (?, ?)', (guild_id, role.id))
        mod_roles_db.commit()
        await interaction.response.send_message(f"Selected role: {role.mention}")

class RoleDropdownView(discord.ui.View):
    def __init__(self, guild_roles):
        super().__init__()
        self.add_item(ModeratorRoleDropdown(guild_roles))

class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Server Moderation', description='Configure server moderation.', emoji='<:icons_unbanmember:866943415321100289>'),
            discord.SelectOption(label='Server Logging', description='Configure server logging.', emoji='🔴')
        ]
        super().__init__(placeholder='Module Configuration', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'Server Moderation':
            view = RoleDropdownView(guild_roles=interaction.guild.roles)
            await interaction.response.send_message('Please select the moderator role!', view=view)

        if self.values[0] == 'Server Logging':
            view = LoggingChannelDropdownView(guild_channels=interaction.guild.channels)
            await interaction.response.send_message('Please select the logging channel!', view=view)

class DropdownView(discord.ui.View):
    def __init__(self, guild_roles):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())

class configure(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.hybrid_command(name="setup", description="Setup x-bot")
    async def setup(self, ctx):
        if ctx.author.guild_permissions.administrator:
            view = DropdownView(guild_roles=ctx.guild.roles)
            embed = discord.Embed(color=discord.Color.blurple(), description="You are now setting up x-bot! Select a module to configure from the dropdown below.\n\n *Have you encountered an error? If so report it in our  [support server](https://discord.gg/26pgMKVwpW)*")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed, view=view)


        

async def setup(client: commands.Bot) -> None:
    await client.add_cog(configure(client))
