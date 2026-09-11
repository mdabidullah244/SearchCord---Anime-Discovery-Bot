import random
import sqlite3
import discord
from discord import app_commands
from discord.ext import commands

random_footer_text = [
    'Wanna search up an Anime or Manga? Use /search',
    'To search up another user use /profile',
    'W.I.P more commands comming soon!'
]

randomstrcolor = [
  '#eee0ca',
  '#e5dfc3',
  '#e5ffe1',
  '#d8eeff',
  '#ffd2d2'
]

class SetUpMangaCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(
        name = 'set_up_manga_info',
        description = 'Set up Manga Info To Your Profile'
    )
    @app_commands.checks.cooldown(1, 15.0, key=lambda i:(i.user.id))
    async def set_up_manga_info(self, ctx: commands.Context):
        username = ctx.user.name
        connection = sqlite3.connect('databases/profile_db.db')
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT username FROM profile_db_info WHERE username = ?', (username,))
            data = cursor.fetchone()
            if data:
                class set_up_manga_info(discord.ui.View):
                    def __init__(self):
                        super().__init__(timeout = None)
                    @discord.ui.button(
                        label = 'Set Up Manga Info',
                        style = discord.ButtonStyle.green
                    )
                    async def set_up_manga_info(self, interaction: discord.Interaction, Button: discord.ui.Button):
                        if interaction.user.id == ctx.user.id:
                            class set_up_manga_modal(discord.ui.Modal, title = 'Set Up Manga Info'):
                                fav_manga = discord.ui.TextInput(
                                    label = 'Fav Manga',
                                    placeholder = 'Your fav Manga',
                                    required = False
                                )
                                manga_read_name = discord.ui.TextInput(
                                    label = 'Manga Read',
                                    placeholder = 'Format: {manga_name}, {manga_name}...',
                                    required = False
                                )
                                manga_reading_name = discord.ui.TextInput(
                                    label = 'Manga Reading',
                                    placeholder = 'Format: {manga_name}, {manga_name}...',
                                    required = False
                                )
                                manga_to_read_name = discord.ui.TextInput(
                                    label = 'Manga To Read',
                                    placeholder = 'Format: {manga_name}, {manga_name}...',
                                    required = False
                                )
                                manga_read_total = discord.ui.TextInput(
                                    label = 'Manga Read In Total',
                                    placeholder = 'Format: {number_of_books}...',
                                    required = False
                                )
                                async def on_submit(self, interaction: discord.Interaction):
                                    fav_manga = self.fav_manga.value
                                    manga_read_name = self.manga_read_name.value
                                    manga_reading_name = self.manga_reading_name.value
                                    manga_to_read_name = self.manga_to_read_name.value
                                    manga_read_total = self.manga_read_total.value
                                    connection = sqlite3.connect('databases/profile_db_m.db')
                                    cursor = connection.cursor()
                                    cursor.execute('SELECT username FROM profile_db_manga_info WHERE username = ?', (username,))
                                    data = cursor.fetchone()
                                    if data:
                                        embed = discord.Embed(
                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Manga Info Already Set Up')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed, view = None)
                                    else:
                                        if manga_read_total.isdigit():
                                            embed = discord.Embed(
                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                timestamp = interaction.created_at
                                            )
                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Manga | Set Up Complete')
                                            embed.set_footer(text = random.choice(random_footer_text))
                                            await interaction.response.edit_message(embed = embed, view = None)
                                            cursor.execute('INSERT INTO profile_db_manga_info (username, fav_manga, manga_read_name, manga_reading_name, manga_to_read_name, manga_read_total) VALUES (?, ?, ?, ?, ?, ?)', (username, fav_manga, manga_read_name, manga_reading_name, manga_to_read_name, manga_read_total))
                                            connection.commit()
                                        else:
                                            embed = discord.Embed(
                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                timestamp = interaction.created_at
                                            )
                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Manga Read In Total Has To Be An Integer')
                                            embed.set_footer(text = random.choice(random_footer_text))
                                            await interaction.response.edit_message(embed = embed, view = None)
                            await interaction.response.send_modal(set_up_manga_modal())
                        else:
                            embed = discord.Embed(
                                color = discord.Color.from_str('#e5ffe1'),
                                timestamp = interaction.created_at
                            )
                            embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                            embed.set_footer(text = random.choice(random_footer_text))
                            await interaction.response.send_message(embed = embed, ephemeral = True)
                    @discord.ui.button(
                        label = 'Exit',
                        style = discord.ButtonStyle.red
                    )
                    async def exit_button(self, interaction: discord.Interaction, Button: discord.ui.Button):
                        if interaction.user.id == ctx.user.id:
                            embed = discord.Embed(
                                color = discord.Color.from_str('#e5ffe1'),
                                timestamp = interaction.created_at
                            )
                            embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Exit Command')
                            embed.set_footer(text = random.choice(random_footer_text))
                            await interaction.response.edit_message(embed = embed, view = None)
                        else:
                            embed = discord.Embed(
                                color = discord.Color.from_str('#e5ffe1'),
                                timestamp = interaction.created_at
                            )
                            embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                            embed.set_footer(text = random.choice(random_footer_text))
                            await interaction.response.send_message(embed = embed, ephemeral = True)
                embed = discord.Embed(
                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                    timestamp = ctx.created_at
                )
                embed.set_author(icon_url = ctx.user.avatar, name = f'Profile | Set Up Manga Info')
                embed.set_footer(text = random.choice(random_footer_text))
                await ctx.response.send_message(embed = embed, view = set_up_manga_info())
            else:
                embed = discord.Embed(
                    color = discord.Color.from_str('#e5ffe1'),
                    timestamp = ctx.created_at
                )
                embed.set_author(icon_url = ctx.user.avatar, name = 'Profile | Profile Not Found')
                embed.set_footer(text = random.choice(random_footer_text))
                await ctx.response.send_message(embed = embed)
        finally:
            connection.close()
    @set_up_manga_info.error
    async def set_up_manga_info_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(
                color = discord.Color.from_str('#eee0ca'),
                timestamp = ctx.created_at
            )
            embed.set_author(icon_url = ctx.user.avatar, name = "This command is on cooldown")
            embed.add_field(name = 'Woah?!', value = 'This command has a big cooldown as multiple people running it at the same time may cause unexpected errors')
            embed.set_footer(text = f'The command will be available in {round(error.retry_after, 2)} | {random.choice(random_footer_text)}')
            await ctx.response.send_message(embed = embed, ephemeral = True)
        else:
            embed = discord.Embed(
                color = discord.Color.from_str('#eee0ca'),
                timestamp = ctx.created_at
            )
            embed.set_author(icon_url = ctx.user.avatar, name = "Uh Oh! Something isn't right here :(")
            embed.set_footer(text = f'We will fix this command ASAP! | {random.choice(random_footer_text)}')
            await ctx.response.send_message(embed = embed, ephemeral = True) 

async def setup(client):
    await client.add_cog(SetUpMangaCog(client))