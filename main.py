import discord
from colorama import Back, Fore, Style
import time
import json
import platform
import requests
import importlib
import discord.ext
from discord.ext import commands
import traceback
from datetime import UTC
from discord import app_commands
from datetime import datetime, timedelta
from pytz import timezone
import os
from datetime import datetime
from settings import *
import datetime
import logging
import sqlite3
import discord
import glob
import asyncio



class XBOT(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(bot_prefix), intents=discord.Intents().all())

        self.cogslist = ["main2.commands.Moderation.test1","main2.events.Member Events.member_join","main2.commands.Moderation.banuser","main2.functions.buttons","main2.commands.Utility.configchange","main2.commands.Utility.dataremoval"]

    async def setup_hook(self):
      for ext in self.cogslist:
        await self.load_extension(ext)

    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S GMT", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        synced = await self.tree.sync()
        print(prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")
        print(prfx + " Bot is in " + Fore.YELLOW + str(len(self.guilds)) + " servers")
        await client.change_presence(activity=discord.Game(name=f"in {len(self.guilds)} servers!"))







    

client = XBOT()

# Define the !role command
@client.command()
async def role(ctx, role: discord.Role):
    # Get the guild ID of the server
    guild_id = ctx.guild.id
    
    # Store the selected role ID as the moderator role for the server
    mod_roles[guild_id] = role.id
    
    # Save the updated mod_roles dictionary to the database
    c_mod_roles.execute('INSERT OR REPLACE INTO mod_roles (guild_id, mod_role_id) VALUES (?, ?)', (guild_id, role.id))
    mod_roles_db.commit()
    
    # Send a confirmation message to the user
    await ctx.send(f"{role.name} has been set as the moderator role for this server.")

# Define the !getmod command
@client.command()
async def getmod(ctx):
    # Get the moderator role for the current server
    mod_role_id = mod_roles.get(ctx.guild.id)
    
    # Check if a moderator role was found
    if mod_role_id is not None:
        # Get the role object for the moderator role
        mod_role = discord.utils.get(ctx.guild.roles, id=mod_role_id)
        
        # Mention the moderator role in a reply to the user
        await ctx.reply(mod_role.mention)
    else:
        # If no moderator role is stored, send an error message
        await ctx.send("No moderator role has been set for this server.")



# Define the !channel command
@client.command()
async def channel(ctx, channel: discord.TextChannel):
    # Get the guild ID of the server
    guild_id = ctx.guild.id
    
    # Store the selected channel ID as the designated channel for the server
    channels[guild_id] = channel.id
    
    # Save the updated channels dictionary to the database
    c_channels.execute('INSERT OR REPLACE INTO channels (guild_id, channel_id) VALUES (?, ?)', (guild_id, channel.id))
    channel_db.commit()
    
    # Send a confirmation message to the user
    await ctx.send(f"{channel.mention} has been set as the designated channel for this server.")

# Define the !getchannel command
@client.command()
async def getchannel(ctx):
    # Get the designated channel for the current server
    channel_id = channels.get(ctx.guild.id)
    
    # Check if a designated channel was found
    if channel_id is not None:
        # Get the channel object for the designated channel
        designated_channel = client.get_channel(channel_id)
        
        # Mention the designated channel in a reply to the user
        await ctx.reply(designated_channel.mention)
    else:
        # If no designated channel is stored, send an error message
        await ctx.send("No designated channel has been set for this server.")



class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Red', description='Your favourite colour is red', emoji='🟥'),
            discord.SelectOption(label='Green', description='Your favourite colour is green', emoji='🟩'),
            discord.SelectOption(label='Blue', description='Your favourite colour is blue', emoji='🟦'),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Choose your favourite colour...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')



class RoleDropdown(discord.ui.Select):
    def __init__(self, guild_roles):
        options = [
            discord.SelectOption(label=f"@{role.name}", value=str(role.id)) for role in guild_roles
        ]
        super().__init__(placeholder='Select a role', options=options)

    async def callback(self, interaction: discord.Interaction):
        role_id = int(self.values[0])
        role = interaction.guild.get_role(role_id)
        c_mod_roles.execute("INSERT OR REPLACE INTO mod_roles (guild_id, mod_role_id) VALUES (?, ?)", (interaction.guild.id, role_id))
        mod_roles_db.commit()
        await interaction.response.send_message(f"Selected role: {role.mention}")

@client.command()
async def testdro(ctx):
    view = discord.ui.View()
    roles_dropdown = RoleDropdown(ctx.guild.roles)
    view.add_item(roles_dropdown)
    await ctx.send('Pick a role:', view=view)

        

class Feedback(discord.ui.Modal, title='Feedback'):
    # Our modal classes MUST subclass `discord.ui.Modal`,
    # but the title can be whatever you want.

    # This will be a short input, where the user can enter their name
    # It will also have a placeholder, as denoted by the `placeholder` kwarg.
    # By default, it is required and is a short-style input which is exactly
    # what we want.
    name = discord.ui.TextInput(
        label='Name',
        placeholder='Your name here...',
    )

    # This is a longer, paragraph style input, where user can submit feedback
    # Unlike the name, it is not required. If filled out, however, it will
    # only accept a maximum of 300 characters, as denoted by the
    # `max_length=300` kwarg.
    feedback = discord.ui.TextInput(
        label='What do you think of this new feature?',
        style=discord.TextStyle.long,
        placeholder='Type your feedback here...',
        required=False,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)





conn = sqlite3.connect('banned_users.db')
c = conn.cursor()

# create the banned_users table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS banned_users (
        user_id INTEGER PRIMARY KEY
    )
''')
conn.commit()

@client.command()
@commands.has_permissions(administrator=True)
async def botban(ctx, user: discord.User):
    """Ban a user from using the bot."""
    c.execute('INSERT OR IGNORE INTO banned_users (user_id) VALUES (?)', (user.id,))
    conn.commit()
    await ctx.send(f"{user.name} has been banned from using the bot.")

@client.command()
async def hi(ctx):
    """Greet the user."""
    user = str(ctx.author)
    c.execute('SELECT * FROM banned_users WHERE user_id=?', (ctx.author.id,))
    if c.fetchone():
        await ctx.send("Sorry, you are banned from using the bot.")
    else:
        await ctx.send(f"Hi {user}!")

@client.command()
@commands.has_permissions(administrator=True)
async def botunban(ctx, user: discord.User):
    """Unban a user from using the bot."""
    c.execute('DELETE FROM banned_users WHERE user_id=?', (user.id,))
    conn.commit()
    await ctx.send(f"{user.name} has been unbanned from using the bot.")



class DataRemovalSelect(discord.ui.Select):
    def __init__(self, server_id: int):
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Moderator Role', description='Remove the moderator role for the selected guild.', emoji='<:icons_banmembers:866943415361732628>'),
            discord.SelectOption(label='Logging Channel', description='Remove the logging channel from the selected guild.', emoji='<:icons_deletechannel:866943415396990987>')
        ]
        super().__init__(placeholder='Data Removal', min_values=1, max_values=1, options=options)
        self.server_id = server_id

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'Moderator Role':
            mod_role_id = mod_roles.get(self.server_id)
            if mod_role_id:
                mod_role = discord.utils.get(interaction.guild.roles, id=mod_role_id)
                c_mod_roles.execute("DELETE FROM mod_roles WHERE guild_id = ?", (self.server_id,))
                mod_roles_db.commit()
                mod_roles.pop(self.server_id, None)
                await interaction.response.send_message(f"Moderator role {mod_role.name} has been removed for server {self.server_id}.")
            else:
                await interaction.response.send_message("No moderator role was set for this server.")

class DataRemovalView(discord.ui.View):
    def __init__(self, server_id):
        super().__init__()
        self.add_item(DataRemovalSelect(server_id))

@client.command()
@commands.has_permissions(administrator=True)
async def dataremove(ctx, server_id: int):
    # Create the select dropdown
    select = DataRemovalView(server_id)

    # Send the message with the dropdown
    message = await ctx.send("Select data to remove:", view=select)


@client.command()
async def moderator(ctx):
    mod_role_id = mod_roles.get(ctx.guild.id)
    if mod_role_id:
        mod_role = discord.utils.get(ctx.guild.roles, id=mod_role_id)
        if mod_role:
            await ctx.send(f"The moderator role for this server is {mod_role.name}.")
            return
    await ctx.send("The moderator role has not been set for this server.")


@client.command()
async def emoj(ctx):
    await ctx.reply("<:discord:1088574023807533252>")


@client.command()
async def serverstats(ctx):
    guild = ctx.guild
    voice_channels = len(guild.voice_channels)
    text_channels = len(guild.text_channels)
    roles = len(guild.roles)
    emojis = len(guild.emojis)
    bans = await guild.fetch_bans()
    ban_count = len(bans)
    created_at = guild.created_at.strftime("%d %b %y")


    owner = guild.owner.mention
    members_online = sum(1 for member in guild.members if member.status != discord.Status.offline)
    members_total = len(guild.members)
    text_channels_count = len(guild.text_channels)
    voice_channels_count = len(guild.voice_channels)
    region = str(guild.region).title()

    embed = discord.Embed(title="X-bot Testing", color=discord.Color.blue())
    embed.add_field(name="Server ID", value=guild.id)
    embed.add_field(name="Owner", value=owner)
    embed.add_field(name="Members", value=f"Online: {members_online} | {members_total - members_online} Members")
    embed.add_field(name="Channels", value=f"Text: {text_channels_count} | Voice:{voice_channels_count} ")
    embed.add_field(name="Roles", value=roles)
    embed.add_field(name="Emojis", value=emojis)
    embed.add_field(name="Voice Region", value=f" {region}")
    embed.add_field(name="Ban Count", value=f" {ban_count}")


    if guild.icon:
        embed.set_thumbnail(url=guild.icon_url)

    await ctx.send(embed=embed)

client.event
async def on_message(message):
    # Check if message is a DM and not sent by bot
    if isinstance(message.channel, discord.DMChannel) and message.author != client.user:
        # Get channel by ID
        channel = client.get_channel(int(1087038043837452428))
        # Send message to channel
        await channel.send(f"New DM from {message.author}: {message.content}")

@client.hybrid_command()
async def hybird(ctx):
    await ctx.send("This is a hybrid command!")

client.run(token)