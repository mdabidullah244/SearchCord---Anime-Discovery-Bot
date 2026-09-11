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

class ProfileCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(
        name = 'profile',
        description = 'View Profile'
    )
    @app_commands.checks.cooldown(1, 10.0, key=lambda i:(i.user.id))
    async def profile(self, ctx: commands.Context, username: str = None):
        date_format = "%a, %b %d, %Y At %I:%M %p"
        created_at_date_format = ctx.user.created_at.strftime(date_format)
        joined_at_date_format = ctx.user.joined_at.strftime(date_format)
        if username == None:
            username = ctx.user.name
            connection = sqlite3.connect('databases/profile_db.db')
            try:
                cursor = connection.cursor()
                cursor.execute('SELECT username FROM profile_db_info WHERE username = ?', (username,))
                data = cursor.fetchone()
                if data:
                    cursor.execute('SELECT bio, gender, birthday FROM profile_db_info WHERE username = ?', (username,))
                    data = cursor.fetchone()
                    bio = data[0]
                    gender = data[1]
                    birthday = data[2]
                    class profile_menu(discord.ui.View):
                        options = [
                            discord.SelectOption(label = 'Profile', value = 'pv', description = 'View Your Profile'),
                            discord.SelectOption(label = 'Anime', value = 'av', description = 'View Your Anime Info'),
                            discord.SelectOption(label = 'Manga', value = 'mv', description = 'View Your Manga Info')
                        ]
                        @discord.ui.select(
                            placeholder = 'Profile Menu',
                            options = options
                        )
                        async def profile_menu_selection(self, interaction: discord.Interaction, select):
                            select.disabled = True
                            if select.values[0] == 'pv':
                                if interaction.user.id == ctx.user.id:
                                    embed = discord.Embed(
                                        title = 'Bio',
                                        description = bio,
                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Info | {username}')
                                    embed.set_thumbnail(url = interaction.user.avatar)
                                    embed.add_field(name = 'Profile Info', value = f'Gender: {gender}\nBirthday: {birthday}', inline = True)
                                    embed.add_field(name = 'User Info', value = f'Created: {created_at_date_format}\nJoined: {joined_at_date_format}')
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.edit_message(embed = embed, view = profile_menu())
                                else:
                                    embed = discord.Embed(
                                        color = discord.Color.from_str('#eee0ca'),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.send_message(embed = embed, ephemeral = True)
                            elif select.values[0] == 'av':
                                if interaction.user.id == ctx.user.id:
                                    connection = sqlite3.connect('databases/profile_db_a.db')
                                    cursor = connection.cursor()
                                    cursor.execute('SELECT username FROM profile_db_anime_info WHERE username = ?', (username,))
                                    data = cursor.fetchone()
                                    if data:
                                        cursor.execute('SELECT fav_anime, anime_watched_name, anime_watching_name, anime_to_watch_name, anime_watched_hours FROM profile_db_anime_info WHERE username = ?', (username,))
                                        data = cursor.fetchone()
                                        fav_anime = data[0]
                                        anime_watched_name = data[1]
                                        anime_watching_name = data[2]
                                        anime_to_watch_name = data[3]
                                        anime_watched_hours = data[4]
                                        hour_days_anime = 24
                                        hour_weeks_anime = 168
                                        hour_months_anime = 730
                                        hour_years_anime = 8760
                                        total_hour_days_anime = int(anime_watched_hours/hour_days_anime)
                                        total_hour_weeks_anime = int(anime_watched_hours/hour_weeks_anime)
                                        total_hour_months_anime = int(anime_watched_hours/hour_months_anime)
                                        total_hour_years_anime = int(anime_watched_hours/hour_years_anime)
                                        embed = discord.Embed(
                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Anime Info | {username}')
                                        embed.set_thumbnail(url = interaction.user.avatar)
                                        embed.add_field(name = 'Fav Anime', value = fav_anime, inline = False)
                                        embed.add_field(name = 'Anime Watched', value = anime_watched_name, inline = False)
                                        embed.add_field(name = 'Anime Watching', value = anime_watching_name, inline = False)
                                        embed.add_field(name = 'Anime To Watch', value = anime_to_watch_name, inline = False)
                                        embed.add_field(name = 'Statistics', value = f'**Hours Watched**\n{anime_watched_hours}\n**Days Watched**\n{total_hour_days_anime}\n**Weeks Watched**\n{total_hour_weeks_anime}\n**Months Watched**\n{total_hour_months_anime}\n**Years Watched**\n{total_hour_years_anime}')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed, view = profile_menu())
                                    else:
                                        embed = discord.Embed(
                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Anime Info Not Set Up | {username}')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed, view = profile_menu())
                                else:
                                    embed = discord.Embed(
                                        color = discord.Color.from_str('#eee0ca'),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.send_message(embed = embed, ephemeral = True)
                            elif select.values[0] == 'mv':
                                if interaction.user.id == ctx.user.id:
                                    connection = sqlite3.connect('databases/profile_db_m.db')
                                    cursor = connection.cursor()
                                    cursor.execute('SELECT username FROM profile_db_manga_info WHERE username = ?', (username,))
                                    data = cursor.fetchone()
                                    if data:
                                        cursor.execute('SELECT fav_manga, manga_read_name, manga_reading_name, manga_to_read_name, manga_read_total FROM profile_db_manga_info WHERE username = ?', (username,))
                                        data = cursor.fetchone()
                                        fav_manga = data[0]
                                        manga_read_name = data[1]
                                        manga_reading_name = data[2]
                                        manga_to_read_name = data[3]
                                        manga_read_total = data[4]
                                        hours_manga = 1.5
                                        hour_days_manga = 24
                                        hour_weeks_manga = 168
                                        hour_months_manga = 730
                                        hour_years_manga = 8760
                                        total_hours_manga = int(manga_read_total*hours_manga)
                                        total_days_manga = int(total_hours_manga/hour_days_manga)
                                        total_weeks_manga = int(total_hours_manga/hour_weeks_manga)
                                        total_months_manga = int(total_hours_manga/hour_months_manga)
                                        total_years_manga = int(total_hours_manga/hour_years_manga)
                                        embed = discord.Embed(
                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Manga Info | {username}')
                                        embed.set_thumbnail(url = interaction.user.avatar)
                                        embed.add_field(name = 'Fav Manga', value = fav_manga, inline = False)
                                        embed.add_field(name = 'Manga Read', value = manga_read_name, inline = False)
                                        embed.add_field(name = 'Manga Reading', value = manga_reading_name, inline = False)
                                        embed.add_field(name = 'Manga To Read', value = manga_to_read_name, inline = False)
                                        embed.add_field(name = 'Statistics', value = f'**Manga Read In Total**\n{manga_read_total}\n**Hours Read**\n{total_hours_manga}\n**Days Read**\n{total_days_manga}\n**Weeks Read**\n{total_weeks_manga}\n**Months Read**\n{total_months_manga}\n**Years Read**\n{total_years_manga}')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed, view = profile_menu())
                                    else:
                                        embed = discord.Embed(
                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Manga Info Not Set Up | {username}')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed, view = profile_menu())
                                else:
                                    embed = discord.Embed(
                                        color = discord.Color.from_str('#eee0ca'),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.send_message(embed = embed, ephemeral = True)
                    embed = discord.Embed(
                        title = 'Bio',
                        description = bio,
                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                        timestamp = ctx.created_at
                    )
                    embed.set_author(icon_url = ctx.user.avatar, name = f'Profile | Info | {username}')
                    embed.set_thumbnail(url = ctx.user.avatar)
                    embed.add_field(name = 'Profile Info', value = f'Gender: {gender}\nBirthday: {birthday}', inline = True)
                    embed.add_field(name = 'User Info', value = f'Created: {created_at_date_format}\nJoined: {joined_at_date_format}')
                    embed.set_footer(text = random.choice(random_footer_text))
                    await ctx.response.send_message(embed = embed, view = profile_menu())
                else:
                    embed = discord.Embed(
                        color = discord.Color.from_str('#e5ffe1'),
                        timestamp = ctx.created_at
                    )
                    embed.set_author(icon_url = ctx.user.avatar, name = 'Profile | Profile Not Set Up')
                    embed.set_footer(text = random.choice(random_footer_text))
                    await ctx.response.send_message(embed = embed)
            finally:
                connection.close()
        elif username == ctx.user.name:
            username = ctx.user.name
            connection = sqlite3.connect('databases/profile_db.db')
            try:
                cursor = connection.cursor()
                cursor.execute('SELECT username FROM profile_db_info WHERE username = ?', (username,))
                data = cursor.fetchone()
                if data:
                    cursor.execute('SELECT bio, gender, birthday FROM profile_db_info WHERE username = ?', (username,))
                    data = cursor.fetchone()
                    bio = data[0]
                    gender = data[1]
                    birthday = data[2]
                    class profile_menu(discord.ui.View):
                        options = [
                            discord.SelectOption(label = 'Profile', value = 'profile_value', description = 'View Your Profile'),
                            discord.SelectOption(label = 'Anime', value = 'anime_value', description = 'View Your Anime Info'),
                            discord.SelectOption(label = 'Manga', value = 'manga_value', description = 'View Your Manga Info')
                        ]
                        @discord.ui.select(
                            placeholder = 'Profile Menu',
                            options = options
                        )
                        async def profile_menu_selection(self, interaction: discord.Interaction, select):
                            select.disabled = True
                            if select.values[0] == 'profile_value':
                                if interaction.user.id == ctx.user.id:
                                    embed = discord.Embed(
                                        title = 'Bio',
                                        description = bio,
                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Info | {username}')
                                    embed.set_thumbnail(url = interaction.user.avatar)
                                    embed.add_field(name = 'Profile Info', value = f'Gender: {gender}\nBirthday: {birthday}', inline = True)
                                    embed.add_field(name = 'User Info', value = f'Created: {created_at_date_format}\nJoined: {joined_at_date_format}')
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.edit_message(embed = embed, view = profile_menu())
                                else:
                                    embed = discord.Embed(
                                        color = discord.Color.from_str('#eee0ca'),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.send_message(embed = embed, ephemeral = True)
                            elif select.values[0] == 'anime_value':
                                if interaction.user.id == ctx.user.id:
                                    connection = sqlite3.connect('databases/profile_db_a.db')
                                    cursor = connection.cursor()
                                    cursor.execute('SELECT username FROM profile_db_anime_info WHERE username = ?', (username,))
                                    data = cursor.fetchone()
                                    if data:
                                        cursor.execute('SELECT fav_anime, anime_watched_name, anime_watching_name, anime_to_watch_name, anime_watched_hours FROM profile_db_anime_info WHERE username = ?', (username,))
                                        data = cursor.fetchone()
                                        fav_anime = data[0]
                                        anime_watched_name = data[1]
                                        anime_watching_name = data[2]
                                        anime_to_watch_name = data[3]
                                        anime_watched_hours = data[4]
                                        hour_days_anime = 24
                                        hour_weeks_anime = 168
                                        hour_months_anime = 730
                                        hour_years_anime = 8760
                                        total_hour_days_anime = int(anime_watched_hours/hour_days_anime)
                                        total_hour_weeks_anime = int(anime_watched_hours/hour_weeks_anime)
                                        total_hour_months_anime = int(anime_watched_hours/hour_months_anime)
                                        total_hour_years_anime = int(anime_watched_hours/hour_years_anime)
                                        embed = discord.Embed(
                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Anime Info | {username}')
                                        embed.set_thumbnail(url = interaction.user.avatar)
                                        embed.add_field(name = 'Fav Anime', value = fav_anime, inline = False)
                                        embed.add_field(name = 'Anime Watched', value = anime_watched_name, inline = False)
                                        embed.add_field(name = 'Anime Watching', value = anime_watching_name, inline = False)
                                        embed.add_field(name = 'Anime To Watch', value = anime_to_watch_name, inline = False)
                                        embed.add_field(name = 'Statistics', value = f'**Hours Watched**\n{anime_watched_hours}\n**Days Watched**\n{total_hour_days_anime}\n**Weeks Watched**\n{total_hour_weeks_anime}\n**Months Watched**\n{total_hour_months_anime}\n**Years Watched**\n{total_hour_years_anime}')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed, view = profile_menu())
                                    else:
                                        embed = discord.Embed(
                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Anime Info Not Set Up | {username}')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        color = discord.Color.from_str('#eee0ca'),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.send_message(embed = embed, ephemeral = True)
                            elif select.values[0] == 'manga_value':
                                if interaction.user.id == ctx.user.id:
                                    connection = sqlite3.connect('databases/profile_db_m.db')
                                    cursor = connection.cursor()
                                    cursor.execute('SELECT username FROM profile_db_manga_info WHERE username = ?', (username,))
                                    data = cursor.fetchone()
                                    if data:
                                        cursor.execute('SELECT fav_manga, manga_read_name, manga_reading_name, manga_to_read_name, manga_read_total FROM profile_db_manga_info WHERE username = ?', (username,))
                                        data = cursor.fetchone()
                                        fav_manga = data[0]
                                        manga_read_name = data[1]
                                        manga_reading_name = data[2]
                                        manga_to_read_name = data[3]
                                        manga_read_total = data[4]
                                        hours_manga = 1.5
                                        hour_days_manga = 24
                                        hour_weeks_manga = 168
                                        hour_months_manga = 730
                                        hour_years_manga = 8760
                                        total_hours_manga = int(manga_read_total*hours_manga)
                                        total_days_manga = int(total_hours_manga/hour_days_manga)
                                        total_weeks_manga = int(total_hours_manga/hour_weeks_manga)
                                        total_months_manga = int(total_hours_manga/hour_months_manga)
                                        total_years_manga = int(total_hours_manga/hour_years_manga)
                                        embed = discord.Embed(
                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Manga Info | {username}')
                                        embed.set_thumbnail(url = interaction.user.avatar)
                                        embed.add_field(name = 'Fav Manga', value = fav_manga, inline = False)
                                        embed.add_field(name = 'Manga Read', value = manga_read_name, inline = False)
                                        embed.add_field(name = 'Manga Reading', value = manga_reading_name, inline = False)
                                        embed.add_field(name = 'Manga To Read', value = manga_to_read_name, inline = False)
                                        embed.add_field(name = 'Statistics', value = f'**Manga Read In Total**\n{manga_read_total}\n**Hours Read**\n{total_hours_manga}\n**Days Read**\n{total_days_manga}\n**Weeks Read**\n{total_weeks_manga}\n**Months Read**\n{total_months_manga}\n**Years Read**\n{total_years_manga}')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed, view = profile_menu())
                                    else:
                                        embed = discord.Embed(
                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Manga Info Not Set Up | {username}')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        color = discord.Color.from_str('#eee0ca'),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.send_message(embed = embed, ephemeral = True)
                    embed = discord.Embed(
                        title = 'Bio',
                        description = bio,
                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                        timestamp = ctx.created_at
                    )
                    embed.set_author(icon_url = ctx.user.avatar, name = f'Profile | Info | {username}')
                    embed.set_thumbnail(url = ctx.user.avatar)
                    embed.add_field(name = 'Profile Info', value = f'Gender: {gender}\nBirthday: {birthday}', inline = True)
                    embed.add_field(name = 'User Info', value = f'Created: {created_at_date_format}\nJoined: {joined_at_date_format}')
                    embed.set_footer(text = random.choice(random_footer_text))
                    await ctx.response.send_message(embed = embed, view = profile_menu())
                else:
                    embed = discord.Embed(
                        color = discord.Color.from_str('#e5ffe1'),
                        timestamp = ctx.created_at
                    )
                    embed.set_author(icon_url = ctx.user.avatar, name = f'Profile | {username} Not Found')
                    embed.set_footer(text = random.choice(random_footer_text))
                    await ctx.response.send_message(embed = embed)
            finally:
                connection.close()
        else:
            connection = sqlite3.connect('databases/profile_db.db')
            try:
                cursor = connection.cursor()
                cursor.execute('SELECT username FROM profile_db_info WHERE username = ?', (username,))
                data = cursor.fetchone()
                if data:
                    cursor.execute('SELECT bio, gender, birthday FROM profile_db_info WHERE username = ?', (username,))
                    data = cursor.fetchone()
                    bio = data[0]
                    gender = data[1]
                    birthday = data[2]
                    class profile_menu(discord.ui.View):
                        options = [
                            discord.SelectOption(label = 'Profile', value = 'profile_value', description = 'View Your Profile'),
                            discord.SelectOption(label = 'Anime', value = 'anime_value', description = 'View Your Anime Info'),
                            discord.SelectOption(label = 'Manga', value = 'manga_value', description = 'View Your Manga Info')
                        ]
                        @discord.ui.select(
                            placeholder = 'Profile Menu',
                            options = options
                        )
                        async def profile_menu_selection(self, interaction: discord.Interaction, select):
                            select.disabled = True
                            if select.values[0] == 'profile_value':
                                if interaction.user.id == ctx.user.id:
                                    date_format = "%a, %b %d, %Y At %I:%M %p"
                                    created_at_date_format = interaction.user.created_at.strftime(date_format)
                                    joined_at_date_format = interaction.user.joined_at.strftime(date_format)
                                    embed = discord.Embed(
                                        title = 'Bio',
                                        description = bio,
                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Info | {username}')
                                    embed.set_thumbnail(url = interaction.user.avatar)
                                    embed.add_field(name = 'Profile Info', value = f'Gender: {gender}\nBirthday: {birthday}', inline = True)
                                    embed.add_field(name = 'User Info', value = f'Created: {created_at_date_format}\nJoined: {joined_at_date_format}')
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.edit_message(embed = embed, view = profile_menu())
                                else:
                                    embed = discord.Embed(
                                        color = discord.Color.from_str('#eee0ca'),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.send_message(embed = embed, ephemeral = True)
                            elif select.values[0] == 'anime_value':
                                if interaction.user.id == ctx.user.id:
                                    connection = sqlite3.connect('databases/profile_db_a.db')
                                    cursor = connection.cursor()
                                    cursor.execute('SELECT username FROM profile_db_anime_info WHERE username = ?', (username,))
                                    data = cursor.fetchone()
                                    if data:
                                        cursor.execute('SELECT fav_anime, anime_watched_name, anime_watching_name, anime_to_watch_name, anime_watched_hours FROM profile_db_anime_info WHERE username = ?', (username,))
                                        data = cursor.fetchone()
                                        fav_anime = data[0]
                                        anime_watched_name = data[1]
                                        anime_watching_name = data[2]
                                        anime_to_watch_name = data[3]
                                        anime_watched_hours = data[4]
                                        hour_days_anime = 24
                                        hour_weeks_anime = 168
                                        hour_months_anime = 730
                                        hour_years_anime = 8760
                                        total_hour_days_anime = int(anime_watched_hours/hour_days_anime)
                                        total_hour_weeks_anime = int(anime_watched_hours/hour_weeks_anime)
                                        total_hour_months_anime = int(anime_watched_hours/hour_months_anime)
                                        total_hour_years_anime = int(anime_watched_hours/hour_years_anime)
                                        embed = discord.Embed(
                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Anime Info | {username}')
                                        embed.set_thumbnail(url = interaction.user.avatar)
                                        embed.add_field(name = 'Fav Anime', value = fav_anime, inline = False)
                                        embed.add_field(name = 'Anime Watched', value = anime_watched_name, inline = False)
                                        embed.add_field(name = 'Anime Watching', value = anime_watching_name, inline = False)
                                        embed.add_field(name = 'Anime To Watch', value = anime_to_watch_name, inline = False)
                                        embed.add_field(name = 'Statistics', value = f'**Hours Watched**\n{anime_watched_hours}\n**Days Watched**\n{total_hour_days_anime}\n**Weeks Watched**\n{total_hour_weeks_anime}\n**Months Watched**\n{total_hour_months_anime}\n**Years Watched**\n{total_hour_years_anime}')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed, view = profile_menu())
                                    else:
                                        embed = discord.Embed(
                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Anime Info Not Set Up | {username}')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        color = discord.Color.from_str('#eee0ca'),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.send_message(embed = embed, ephemeral = True)
                            elif select.values[0] == 'manga_value':
                                if interaction.user.id == ctx.user.id:
                                    connection = sqlite3.connect('databases/profile_db_m.db')
                                    cursor = connection.cursor()
                                    cursor.execute('SELECT username FROM profile_db_manga_info WHERE username = ?', (username,))
                                    data = cursor.fetchone()
                                    if data:
                                        cursor.execute('SELECT fav_manga, manga_read_name, manga_reading_name, manga_to_read_name, manga_read_total FROM profile_db_manga_info WHERE username = ?', (username,))
                                        data = cursor.fetchone()
                                        fav_manga = data[0]
                                        manga_read_name = data[1]
                                        manga_reading_name = data[2]
                                        manga_to_read_name = data[3]
                                        manga_read_total = data[4]
                                        hours_manga = 1.5
                                        hour_days_manga = 24
                                        hour_weeks_manga = 168
                                        hour_months_manga = 730
                                        hour_years_manga = 8760
                                        total_hours_manga = int(manga_read_total*hours_manga)
                                        total_days_manga = int(total_hours_manga/hour_days_manga)
                                        total_weeks_manga = int(total_hours_manga/hour_weeks_manga)
                                        total_months_manga = int(total_hours_manga/hour_months_manga)
                                        total_years_manga = int(total_hours_manga/hour_years_manga)
                                        embed = discord.Embed(
                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Manga Info | {username}')
                                        embed.set_thumbnail(url = interaction.user.avatar)
                                        embed.add_field(name = 'Fav Manga', value = fav_manga, inline = False)
                                        embed.add_field(name = 'Manga Read', value = manga_read_name, inline = False)
                                        embed.add_field(name = 'Manga Reading', value = manga_reading_name, inline = False)
                                        embed.add_field(name = 'Manga To Read', value = manga_to_read_name, inline = False)
                                        embed.add_field(name = 'Statistics', value = f'**Manga Read In Total**\n{manga_read_total}\n**Hours Read**\n{total_hours_manga}\n**Days Read**\n{total_days_manga}\n**Weeks Read**\n{total_weeks_manga}\n**Months Read**\n{total_months_manga}\n**Years Read**\n{total_years_manga}')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed, view = profile_menu())
                                    else:
                                        embed = discord.Embed(
                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Profile | Manga Info Not Set Up | {username}')
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.edit_message(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        color = discord.Color.from_str('#eee0ca'),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.send_message(embed = embed, ephemeral = True)
                    embed = discord.Embed(
                        title = 'Bio',
                        description = bio,
                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                        timestamp = ctx.created_at
                    )
                    embed.set_author(icon_url = ctx.user.avatar, name = f'Profile | Info | {username}')
                    embed.set_thumbnail(url = ctx.user.avatar)
                    embed.add_field(name = 'Profile Info', value = f'Gender: {gender}\nBirthday: {birthday}', inline = True)
                    embed.add_field(name = 'User Info', value = f'Created: {created_at_date_format}\nJoined: {joined_at_date_format}')
                    embed.set_footer(text = random.choice(random_footer_text))
                    await ctx.response.send_message(embed = embed, view = profile_menu())
                else:
                    embed = discord.Embed(
                        color = discord.Color.from_str('#e5ffe1'),
                        timestamp = ctx.created_at
                    )
                    embed.set_author(icon_url = ctx.user.avatar, name = f'Profile | {username} Not Found')
                    embed.set_footer(text = random.choice(random_footer_text))
                    await ctx.response.send_message(embed = embed)
            finally:
                connection.close()
    @profile.error
    async def profile_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(
                color = discord.Color.from_str('#eee0ca'),
                timestamp = ctx.created_at
            )
            embed.set_author(icon_url = ctx.user.avatar, name = "This command is on cooldown")
            embed.add_field(name = 'Woah?!', value = 'This command has a cooldown as multiple people running it at the same time may cause unexpected errors')
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
    await client.add_cog(ProfileCog(client))