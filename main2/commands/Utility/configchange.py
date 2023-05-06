import discord
import random
from discord import Embed, app_commands
from discord.ext import commands
import discord.ext
import discord.ui
from settings import *


class LoggingChannelDropdown(discord.ui.Select):
    def __init__(self, guild_channels):
        options = [
            discord.SelectOption(label=f"Member Logging", value=LoggingChannelType.MEMBER.value),
            discord.SelectOption(label=f"Channel Logging", value=LoggingChannelType.CHANNEL.value),
            discord.SelectOption(label=f"Role Logging", value=LoggingChannelType.ROLE.value),
            discord.SelectOption(label=f"Message Logging", value=LoggingChannelType.MESSAGE.value)
        ]
        super().__init__(placeholder='Select what logging type to configure.', options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == LoggingChannelType.MEMBER.value:
            member_logging_dropdown = LoggingMemberOptionDropdown(interaction.guild.channels)
            member_logging_view = discord.ui.View()
            member_logging_view.add_item(member_logging_dropdown)
            await interaction.response.send_message(view=member_logging_view, ephemeral=True)
        elif self.values[0] == LoggingChannelType.CHANNEL.value:
            channel_logging_dropdown = LoggingChannelEventOptionDropdown(interaction.guild.channels)
            channel_logging_view = discord.ui.View()
            channel_logging_view.add_item(channel_logging_dropdown)
            await interaction.response.send_message(view=channel_logging_view, ephemeral=True)
            pass
        elif self.values[0] == LoggingChannelType.ROLE.value:
            role_logging_dropdown = LoggingRoleEventDropdown(interaction.guild.channels)
            role_logging_view = discord.ui.View()
            role_logging_view.add_item(role_logging_dropdown)
            await interaction.response.send_message(view=role_logging_view, ephemeral=True)
            pass
        elif self.values[0] == LoggingChannelType.MESSAGE.value:
            message_logging_dropdown = LoggingMessageEventOptionDropdown(interaction.guild.channels)
            message_logging_view = discord.ui.View()
            message_logging_view.add_item(message_logging_dropdown)
            await interaction.response.send_message(view=message_logging_view, ephemeral=True)
            pass

class LoggingMemberOptionDropdown(discord.ui.ChannelSelect):
    def __init__(self, guild_channels):
        super().__init__(placeholder='Select where to log member evetns.', max_values=1, min_values=1)
        self.guild_channels = guild_channels

    async def callback(self, interaction: discord.Interaction):
        channel_id = int(self.values[0].id)
        channel = interaction.guild.get_channel(channel_id)
        guild_id = interaction.guild.id
        member_log_channels[guild_id] = channel.id
        c_channels.execute('INSERT OR REPLACE INTO log_channels (guild_id, channel_id, type) VALUES (?, ?, ?)', (guild_id, channel.id, LoggingChannelType.MEMBER.value))
        channel_db.commit()
        await interaction.response.send_message(f"Selected member events logging: {channel.mention}", ephemeral=True)

class LoggingChannelEventOptionDropdown(discord.ui.ChannelSelect):
    def __init__(self, guild_channels):
        super().__init__(placeholder='Select where to log channel events.', max_values=1, min_values=1)
        self.guild_channels = guild_channels

    async def callback(self, interaction: discord.Interaction):
        channel_id = int(self.values[0].id)
        channel = interaction.guild.get_channel(channel_id)
        guild_id = interaction.guild.id
        channel_log_channels[guild_id] = channel.id
        c_channels.execute('INSERT OR REPLACE INTO log_channels (guild_id, channel_id, type) VALUES (?, ?, ?)', (guild_id, channel.id, LoggingChannelType.CHANNEL.value))
        channel_db.commit()
        await interaction.response.send_message(f"Selected channel events logging: {channel.mention}")


class LoggingRoleEventDropdown(discord.ui.ChannelSelect):
    def __init__(self, guild_channels):
        super().__init__(placeholder='Select where to log role events.', max_values=1, min_values=1)
        self.guild_channels = guild_channels

    async def callback(self, interaction: discord.Interaction):
        channel_id = int(self.values[0].id)
        channel = interaction.guild.get_channel(channel_id)
        guild_id = interaction.guild.id
        role_log_channels[guild_id] = channel.id
        c_channels.execute('INSERT OR REPLACE INTO log_channels (guild_id, channel_id, type) VALUES (?, ?, ?)', (guild_id, channel.id, LoggingChannelType.ROLE.value))
        channel_db.commit()
        await interaction.response.send_message(f"Selected role events logging: {channel.mention}")

class LoggingMemberEventDropdown(discord.ui.ChannelSelect):
    def __init__(self, guild_channels):
        super().__init__(placeholder='Select where to log message events.', max_values=1, min_values=1)
        self.guild_channels = guild_channels

    async def callback(self, interaction: discord.Interaction):
        channel_id = int(self.values[0].id)
        channel = interaction.guild.get_channel(channel_id)
        guild_id = interaction.guild.id
        message_log_channels[guild_id] = channel.id
        c_channels.execute('INSERT OR REPLACE INTO log_channels (guild_id, channel_id, type) VALUES (?, ?, ?)', (guild_id, channel.id, LoggingChannelType.MESSAGE.value))
        channel_db.commit()
        await interaction.response.send_message(f"Selected message events logging: {channel.mention}")

class LoggingMessageEventOptionDropdown(discord.ui.ChannelSelect):
    def __init__(self, guild_channels):
        super().__init__(placeholder='Select where to log message events.', max_values=1, min_values=1)
        self.guild_channels = guild_channels

    async def callback(self, interaction: discord.Interaction):
        channel_id = int(self.values[0].id)
        channel = interaction.guild.get_channel(channel_id)
        guild_id = interaction.guild.id
        message_log_channels[guild_id] = channel.id
        c_channels.execute('INSERT OR REPLACE INTO log_channels (guild_id, channel_id, type) VALUES (?, ?, ?)', (guild_id, channel.id, LoggingChannelType.MESSAGE.value))
        channel_db.commit()
        await interaction.response.send_message(f"Selected message events logging: {channel.mention}")


class LoggingChannelDropdownView(discord.ui.View):
    def __init__(self, guild_channels):
        super().__init__()
        self.add_item(LoggingChannelDropdown(guild_channels))

#--------------------------------------------------------------------------------------------------------------------------------------------#

class WelcomeChannelDropdownSelect(discord.ui.Select):
    def __init__(self, guild_channels):
        options = [
            discord.SelectOption(label=f"#{channel.name}", value=str(channel.id)) for channel in guild_channels

        ]
        super().__init__(placeholder='Configure server welcoming.', options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == f'#{channel.name}':
            channel_id = int(self.values[0])
            channel = interaction.guild.get_channel(channel_id)
            guild_id = interaction.guild.id
            welcomechannels[guild_id] = channel.id
            w_channels.execute('INSERT OR REPLACE INTO channels (guild_id, channel_id) VALUES (?, ?)', (guild_id, channel.id))
            welcomechannels.commit()
            await interaction.response.send_message(f"Selected welcome channel: {channel.mention}")

class WelcomeChannelDropdownView(discord.ui.View):
    def __init__(self, guild_channels):
        super().__init__()
        self.add_item(WelcomeChannelDropdownSelect(guild_channels))


#--------------------------------------------------------------------------------------------------------------------------------------------#


class ModeratorRoleDropdown(discord.ui.RoleSelect):
    def __init__(self, guild_roles):
        super().__init__(placeholder='Select a role')

    async def callback(self, interaction: discord.Interaction):
        role = self.values[0]
        guild_id = interaction.guild.id
        mod_roles[guild_id] = role.id
        c_mod_roles.execute('INSERT OR REPLACE INTO mod_roles (guild_id, mod_role_id) VALUES (?, ?)', (guild_id, role.id))
        mod_roles_db.commit()
        await interaction.response.send_message(f"Selected role: {role.mention}")


class ModeratorRoleDropdownView(discord.ui.View):
    def __init__(self, guild_roles):
        super().__init__()
        self.add_item(ModeratorRoleDropdown(guild_roles))


#--------------------------------------------------------------------------------------------------------------------------------------------#

class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Server Moderation', description='Configure server moderation.'),
            discord.SelectOption(label='Server Logging', description='Configure server logging.'),
            discord.SelectOption(label='Server Welcoming', description='Configure server welcoming.')
        ]
        super().__init__(placeholder='Module Configuration', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'Server Moderation':
            view = ModeratorRoleDropdownView(guild_roles=interaction.guild.roles)
            await interaction.response.send_message('Please select the moderator role!', ephemeral=True, view=view)


        if self.values[0] == 'Server Logging':
            view = LoggingChannelDropdownView(guild_channels=interaction.guild.channels)
            await interaction.response.send_message('Please select the logging channel!', view=view, ephemeral=True)

        if self.values[0] == 'Server Logging':
            view = LoggingChannelDropdownView(guild_channels=interaction.guild.channels)
            await interaction.response.send_message('Please select the welcome channel!', view=view, ephemeral=True)

class DropdownView(discord.ui.View):
    def __init__(self, guild_roles):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())

#--------------------------------------------------------------------------------------------------------------------------------------------#

class configure(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @app_commands.command(name="config-set", description="Setup x-bot")
    async def setup(self, interaction: discord.Interaction):
         if interaction.guild.get_member(interaction.user.id).guild_permissions.administrator:
            view = DropdownView(guild_roles=interaction.guild.roles)
            embed = discord.Embed(color=discord.Color.blurple(), description="You are now setting up x-bot! Select a module to configure from the dropdown below.\n\n *Have you encountered an error? If so report it in our  [support server](https://discord.gg/26pgMKVwpW)*")
            embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True, view=view)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(configure(client))
