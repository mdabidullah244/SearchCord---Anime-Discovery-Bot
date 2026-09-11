import os
import asyncio
import sqlite3
import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '~', intents = discord.Intents.all())
@client.event
async def on_ready():
   await client.change_presence(activity = discord.Streaming(name = f'{len(client.guilds)} servers!', url = 'https://www.twitch.tv/roses_buds'))
   synced = await client.tree.sync()
   print(f'{client.user.name} Status: Online | Synced {len(synced)} Commands')

'''profile_db_connection = sqlite3.connect('databases/profile_db.db')
profile_db_cursor = profile_db_connection.cursor()
profile_db_cursor.execute('CREATE TABLE IF NOT EXISTS profile_db_info (username STRING PRIMARY KEY, bio STRING, gender STRING, birthday STRING)'                                                                          )
profile_db_connection.commit()

profile_db_a_connection = sqlite3.connect('databases/profile_db_a.db')
profile_db_a_cursor = profile_db_a_connection.cursor()
profile_db_a_cursor.execute('CREATE TABLE IF NOT EXISTS profile_db_anime_info (username STRING PRIMARY KEY, fav_anime STRING, anime_watched_name STRING, anime_watching_name STRING, anime_to_watch_name STRING, anime_watched_hours INTEGER)')
profile_db_a_connection.commit()

profile_db_m_connection = sqlite3.connect('databases/profile_db_m.db')
profile_db_m_cursor = profile_db_m_connection.cursor()
profile_db_m_cursor.execute('CREATE TABLE IF NOT EXISTS profile_db_manga_info (username STRING PRIMARY KEY, fav_manga STRING, manga_read_name STRING, manga_reading_name STRING, manga_to_read_name STRING, manga_read_total INTEGER)')
profile_db_m_connection.commit()'''

with open('token.txt') as file:
   token = file.read()

async def load():
   for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
         await client.load_extension(f'cogs.{filename[:-3]}')
async def main():
   async with client:
      await load()
      await client.start(token)

asyncio.run(main())