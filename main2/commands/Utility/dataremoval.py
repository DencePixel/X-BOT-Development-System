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
from discord import app_commands
import os
from settings import *
import logging
import sqlite3
import discord
import glob
import asyncio











class DataRemovalSelect(discord.ui.Select):
    def __init__(self, server_id: int):
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Moderator Role', description='Remove the moderator role for the selected guild.', emoji='<:ModeratorIcon:1092737788782329947>'),
            discord.SelectOption(label='Logging Channel', description='Remove the logging channel from the selected guild.', emoji='<:Channel:1092737774890786836>')
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
                await interaction.response.send_message(f"Moderator role {mod_role} has been removed for server {self.server_id}.")
            else:
                await interaction.response.send_message("No moderator role was set for this server.")

class DataRemovalView(discord.ui.View):
    def __init__(self, server_id):
        super().__init__()
        self.add_item(DataRemovalSelect(server_id))

class DataRemoval(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removedata(self, ctx, server_id: int):
        # Create the select dropdown
        select = DataRemovalView(server_id)

        # Send the message with the dropdown
        message = await ctx.send("Select data to remove:", view=select)

async def setup(client):
    await client.add_cog(DataRemoval(client))