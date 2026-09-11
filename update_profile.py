import random
import re
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

class UpdateProfileCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(
        name = 'update_profile',
        description = 'Update Your Profile'
    )
    @app_commands.checks.cooldown(1, 15.0, key=lambda i:(i.user.id))
    async def update_profile(self, ctx: commands.Context):
        username = ctx.user.name
        connection = sqlite3.connect('databases/profile_db.db')
        cursor = connection.cursor()
        cursor.execute('SELECT username FROM profile_db_info WHERE username = ?', (username,))
        data = cursor.fetchone()
        if data:
            class update_profile_menu(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout = None)
                @discord.ui.button(
                    label = 'Profile Info',
                    style = discord.ButtonStyle.green
                )
                async def update_profile_button(self, interaction: discord.Interaction, Button: discord.ui.Button):
                    if interaction.user.id == ctx.user.id:
                        class update_profile_modal(discord.ui.Modal, title = 'Update Profile Info'):
                            bio = discord.ui.TextInput(
                                label = 'Update Bio',
                                placeholder = 'Update Your Bio Info',
                                style = discord.TextStyle.paragraph,
                                required = True
                            )
                            gender = discord.ui.TextInput(
                                label = 'Update Gender',
                                placeholder = 'Update Your Gender Info',
                                required = True
                            )
                            birthday = discord.ui.TextInput(
                                label = 'Update Birthday',
                                placeholder = 'Update Your Birthday Info',
                                required = True
                            )
                            async def on_submit(self, interaction: discord.Interaction):
                                bio = self.bio.value
                                gender = self.gender.value
                                birthday = self.birthday.value
                                embed = discord.Embed(
                                    color = discord.Color.from_str('#ffd2d2'),
                                    timestamp = interaction.created_at
                                )
                                embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Profile Info Updated')
                                embed.set_footer(text = random.choice(random_footer_text))
                                await interaction.response.edit_message(embed = embed)
                                cursor.execute('UPDATE profile_db_info SET bio = ?, gender = ?, birthday = ? WHERE username = ?', (bio, gender, birthday, username))
                                connection.commit()
                        await interaction.response.send_modal(update_profile_modal())
                    else:
                        embed = discord.Embed(
                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.send_message(embed = embed, ephemeral = True)
                @discord.ui.button(
                    label = 'Anime Info',
                    style = discord.ButtonStyle.green
                )
                async def update_anime_button(self, interaction: discord.Interaction, Button: discord.ui.Button):
                    if interaction.user.id == ctx.user.id:
                        class update_anime_modal(discord.ui.Modal, title = 'Update Anime Info'):
                            fav_anime = discord.ui.TextInput(
                                label = 'Update Fav Anime',
                                placeholder = 'Update Your Fav Anime',
                                required = False
                            )
                            anime_watched_name = discord.ui.TextInput(
                                label = 'Update Anime Watched',
                                placeholder = 'Format: {anime_name},{anime_name}...',
                                required = False
                            )
                            anime_watching_name = discord.ui.TextInput(
                                label = 'Update Anime Watching',
                                placeholder = 'Format: {anime_name},{anime_name}...',
                                required = False
                            )
                            anime_to_watch_name = discord.ui.TextInput(
                                label = 'Update Anime To Watch',
                                placeholder = 'Format: {anime_name},{anime_name}...',
                                required = False
                            )
                            anime_watched_hours = discord.ui.TextInput(
                                label = 'Update Anime Watched Hours',
                                placeholder = 'Format: {hours}...',
                                required = False
                            )
                            async def on_submit(self, interaction: discord.Interaction):
                                connection = sqlite3.connect('databases/profile_db_a.db')
                                cursor = connection.cursor()
                                cursor.execute('SELECT username FROM profile_db_anime_info WHERE username = ?', (username,))
                                data = cursor.fetchone()
                                if data:
                                    updates = {
                                        'fav_anime': self.fav_anime.value,
                                        'anime_watched_name': self.anime_watched_name.value,
                                        'anime_watching_name': self.anime_watching_name.value,
                                        'anime_to_watch_name': self.anime_to_watch_name.value,
                                        'anime_watched_hours': self.anime_watched_hours.value
                                    }
                                    updated_fields = [field for field, value in updates.items() if value and (field != 'anime_watched_hours' or value.isdigit())]
                                    if updated_fields:
                                        embed = discord.Embed(
                                            color = discord.Color.from_str('#ffd2d2'),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Anime Info Updated')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed)
                                        placeholders = ', '.join([f'{field} = ?' for field in updated_fields])
                                        values = [updates[field] for field in updated_fields] + [username]
                                        cursor.execute(f'UPDATE profile_db_anime_info SET {placeholders} WHERE username = ?', values)
                                        connection.commit()
                                    else:
                                        embed = discord.Embed(
                                            color = discord.Color.from_str('#ffd2d2'),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Anime Hours Has To Be An Integer')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        color = discord.Color.from_str('#ffd2d2'),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Anime Info Not Setup')
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.edit_message(embed = embed)
                        await interaction.response.send_modal(update_anime_modal())
                    else:
                        embed = discord.Embed(
                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.send_message(embed = embed, ephemeral = True) 
                @discord.ui.button(
                    label = 'Manga Info',
                    style = discord.ButtonStyle.green
                )
                async def update_manga_button(self, interaction: discord.Interaction, Button: discord.ui.Button):
                    if interaction.user.id == ctx.user.id:
                        class update_anime_modal(discord.ui.Modal, title = 'Update Manga Info'):
                            fav_manga = discord.ui.TextInput(
                                label = 'Update Fav Manga',
                                placeholder = 'Update Your Fav Manga',
                                required = False
                            )
                            manga_read_name = discord.ui.TextInput(
                                label = 'Update Manga Read',
                                placeholder = 'Format: {manga_name},{manga_name}...',
                                required = False
                            )
                            manga_reading_name = discord.ui.TextInput(
                                label = 'Update Manga Reading',
                                placeholder = 'Format: {manga_name},{manga_name}...',
                                required = False
                            )
                            manga_to_read_name = discord.ui.TextInput(
                                label = 'Update Manga To Read',
                                placeholder = 'Format: {manga_name},{manga_name}...',
                                required = False
                            )
                            manga_read_total = discord.ui.TextInput(
                                label = 'Update Manga Read Total',
                                placeholder = 'Format: {number_of_books}...',
                                required = False
                            )
                            async def on_submit(self, interaction: discord.Interaction):
                                connection = sqlite3.connect('databases/profile_db_m.db')
                                cursor = connection.cursor()
                                cursor.execute('SELECT username FROM profile_db_manga_info WHERE username = ?', (username,))
                                data = cursor.fetchone()
                                if data:
                                    updates = {
                                        'fav_manga': self.fav_manga.value,
                                        'manga_read_name': self.manga_read_name.value,
                                        'manga_reading_name': self.manga_reading_name.value,
                                        'manga_to_read_name': self.manga_to_read_name.value,
                                        'manga_read_total': self.manga_read_total.value
                                    }
                                    updated_fields = [field for field, value in updates.items() if value and (field != 'manga_read_total' or value.isdigit())]
                                    if updated_fields:
                                        embed = discord.Embed(
                                            color = discord.Color.from_str('#ffd2d2'),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Manga Info Updated')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed)
                                        placeholders = ', '.join([f'{field} = ?' for field in updated_fields])
                                        values = [updates[field] for field in updated_fields] + [username]
                                        cursor.execute(f'UPDATE profile_db_manga_info SET {placeholders} WHERE username = ?', values)
                                        connection.commit()
                                    else:
                                        embed = discord.Embed(
                                            color = discord.Color.from_str('#ffd2d2'),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Manga Read Total Has To Be An Integer')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        color = discord.Color.from_str('#ffd2d2'),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Manga Info Not Setup')
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.edit_message(embed = embed)
                        await interaction.response.send_modal(update_anime_modal())
                    else:
                        embed = discord.Embed(
                            color = discord.Color.from_str(random.choice(randomstrcolor)),
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
                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Exit Command')
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.edit_message(embed = embed, view = None)
                    else:
                        embed = discord.Embed(
                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.send_message(embed = embed, ephemeral = True)
            embed = discord.Embed(
                color = discord.Color.from_str('#ffd2d2'),
                timestamp = ctx.created_at
            )
            embed.set_author(icon_url = ctx.user.avatar, name = 'Profile | Update Profile Anime Manga')
            embed.set_footer(text = random.choice(random_footer_text))
            await ctx.response.send_message(embed = embed, view = update_profile_menu())
        else:
            embed = discord.Embed(
                color = discord.Color.from_str('#ffd2d2'),
                timestamp = ctx.created_at
            )
            embed.set_author(icon_url = ctx.user.avatar, name = 'Profile | No Profile Setup')
            embed.set_footer(text = random.choice(random_footer_text))
            await ctx.response.send_message(embed = embed)
    @update_profile.error
    async def update_profile_error(self, ctx: commands.Context, error: Exception):
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
    await client.add_cog(UpdateProfileCog(client))