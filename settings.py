import sqlite3
import os
import logging

#--- Bot Secrets Configuration ---#
token = ""
bot_prefix = "!"

#--- Anything Here ---#

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') #--- Logs errors in discord.log file. DO NOT DELETE AT ANY COSTS. ---#

#--------------------------#
mod_dir_parth = os.path.dirname(os.path.realpath(__file__))
mod_roles_db = sqlite3.connect(os.path.join(mod_dir_parth, 'databases', 'mod_role.db'))
c_mod_roles = mod_roles_db.cursor()

c_mod_roles.execute('''CREATE TABLE IF NOT EXISTS mod_roles
             (guild_id INTEGER PRIMARY KEY, mod_role_id INTEGER)''')

mod_roles = {}
c_mod_roles.execute('SELECT guild_id, mod_role_id FROM mod_roles')
for row in c_mod_roles.fetchall():
    mod_roles[row[0]] = row[1]

#--------------------------#
log_dir_path = os.path.dirname(os.path.realpath(__file__))
channel_db = sqlite3.connect(os.path.join(log_dir_path, 'databases', 'log_channel.db'))
c_channels = channel_db.cursor()


c_channels.execute('''CREATE TABLE IF NOT EXISTS channels
             (guild_id INTEGER PRIMARY KEY, channel_id INTEGER)''')


channels = {}
c_channels.execute('SELECT guild_id, channel_id FROM channels')
for row in c_channels.fetchall():
    channels[row[0]] = row[1]

#--------------------------#

wel_dir_path = os.path.dirname(os.path.realpath(__file__))
welcome_db = sqlite3.connect(os.path.join(log_dir_path, 'databases', 'welcome.db'))
w_channels = welcome_db.cursor()


w_channels.execute('''CREATE TABLE IF NOT EXISTS channels
             (guild_id INTEGER PRIMARY KEY, channel_id INTEGER)''')


welcomechannels = {}
w_channels.execute('SELECT guild_id, channel_id FROM channels')
for row in w_channels.fetchall():
    welcomechannels[row[0]] = row[1]

#--------------------------#


banned_users_dic = {"1":"twat"}
