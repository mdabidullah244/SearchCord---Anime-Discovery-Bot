import random
import aiohttp
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

animeapi = 'https://api.jikan.moe/v4/anime?q='
mangaapi = 'https://api.jikan.moe/v4/manga?q='
characterapi = 'https://api.jikan.moe/v4/characters?q='

class SearchCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(
        name = 'search',
        description = 'Search An Anime, Manga, Or Character!'
    )
    @app_commands.checks.cooldown(1, 30.0, key=lambda i:(i.user.id))
    async def search(self, ctx: commands.Command):
        class search_menu(discord.ui.View):
            options = [
                discord.SelectOption(label = 'Anime', value = 'a', description = 'Search for an Anime'),
                discord.SelectOption(label = 'Manga', value = 'm', description = 'Search for a Manga'),
                discord.SelectOption(label = 'Character', value = 'c', description = 'Search for a Character')
            ]
            @discord.ui.select(
                placeholder = 'Search Menu',
                options = options
            )
            async def search_menu_selection(self, interaction: discord.Interaction, select):
                select.disabled = True
                if select.values[0] == 'a':
                    if interaction.user.id == ctx.user.id:
                        class search_modal(discord.ui.Modal, title = 'Search Modal'):
                            anime_name = discord.ui.TextInput(
                                label = 'Search',
                                placeholder = 'Anime Name',
                                required = True
                            )
                            async def on_submit(self, interaction: discord.Interaction):
                                anime_name = self.anime_name.value
                                urlapi = animeapi + anime_name
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(urlapi) as resp:
                                        if resp.status == 200:
                                            jsondata = await resp.json()
                                            data = jsondata['data']
                                            if data:
                                                data = jsondata['data'][0]
                                                pagination = jsondata['pagination']['items']['count']
                                                image_url = data['images']['jpg']['image_url']
                                                title_english = data['title_english']
                                                title_japanese = data['title_japanese']
                                                synopsis = data['synopsis']
                                                rating = data['rating']
                                                if rating == 'Rx - Hentai':
                                                    if interaction.channel.guild:
                                                        if interaction.channel.nsfw:
                                                            class anime_pagination_system(discord.ui.View):
                                                                current_page = 1
                                                                current_search_page = 0
                                                                def __init__(self):
                                                                    super().__init__(timeout = None)
                                                                @discord.ui.button(
                                                                    label = '<<',
                                                                    style = discord.ButtonStyle.blurple
                                                                )
                                                                async def lb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                                    if interaction.user.id == ctx.user.id:
                                                                        if self.current_search_page > 0:
                                                                            self.current_search_page -= 1
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            image_url = data['images']['jpg']['image_url']
                                                                            title_english = data['title_english']
                                                                            title_japanese = data['title_japanese']
                                                                            synopsis = data['synopsis']
                                                                            rating = data['rating']
                                                                            if rating == 'Rx - Hentai':
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            title = f'{title_english} | {title_japanese}',
                                                                                            description = synopsis,
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                        embed.set_thumbnail(url = image_url)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()  
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                                    embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        elif self.current_search_page == 0:
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            image_url = data['images']['jpg']['image_url']
                                                                            title_english = data['title_english']
                                                                            title_japanese = data['title_japanese']
                                                                            synopsis = data['synopsis']
                                                                            rating = data['rating']
                                                                            if rating == 'Rx - Hentai':
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            title = f'{title_english} | {title_japanese}',
                                                                                            description = synopsis,
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                        embed.set_thumbnail(url = image_url)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                                    embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                        await interaction.response.send_message(embed = embed, ephemeral = True)
                                                                @discord.ui.button(
                                                                    label = '<',
                                                                    style = discord.ButtonStyle.green
                                                                )
                                                                async def pb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                                    if interaction.user.id == ctx.user.id:
                                                                        if self.current_page > 1:
                                                                            self.current_page -= 1
                                                                        if self.current_page == 1:
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            image_url = data['images']['jpg']['image_url']
                                                                            title_english = data['title_english']
                                                                            title_japanese = data['title_japanese']
                                                                            synopsis = data['synopsis']
                                                                            rating = data['rating']
                                                                            if rating == 'Rx - Hentai':
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            title = f'{title_english} | {title_japanese}',
                                                                                            description = synopsis,
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                        embed.set_thumbnail(url = image_url)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                                    embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    title = f''
                                                                                )
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        elif self.current_page == 2:
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            trailer_url = data['trailer']['url']
                                                                            trailer_image = data['trailer']['images']['image_url']
                                                                            title_english = data['title_english']
                                                                            title_japanese = data['title_japanese']
                                                                            background = data['background']
                                                                            source = data['source']
                                                                            episodes = data['episodes']
                                                                            status = data['status']
                                                                            airing = data['airing']
                                                                            aired = data['aired']['string']
                                                                            duration = data['duration']
                                                                            released_year = data['year']
                                                                            broadcast = data['broadcast']['string']
                                                                            genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                            themes = ' | '.join([theme['name'] for theme in data['themes']])
                                                                            demographics = ' | '.join([demographic['name'] for demographic in data['demographics']])
                                                                            if trailer_url == 'null':
                                                                                trailer_url = 'None'
                                                                            if trailer_image == 'null':
                                                                                trailer_image = data['images']['jpg']['image_url']
                                                                            if background == '':
                                                                                background = 'None'
                                                                            if genres == '':
                                                                                genres = 'None'
                                                                            if themes == '':
                                                                                themes = 'None'
                                                                            if demographics == '':
                                                                                demographics = 'None'
                                                                            rating = data['rating']
                                                                            if rating == 'Rx - Hentai':
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            title = f'{title_english} | {title_japanese}',
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                        embed.set_thumbnail(url = trailer_image)
                                                                                        embed.add_field(name = 'Background', value = background, inline = False)
                                                                                        embed.add_field(name = 'Info', value = f'Episodes: {episodes}\nDuration {duration}\nYear Released: {released_year}\nBroadcasts: {broadcast}\nSource: {source}\nStatus: {status}\nAiring: {airing}\nAired: {aired}')
                                                                                        embed.add_field(name = 'Trailer', value = trailer_url, inline = False)
                                                                                        embed.add_field(name = 'Genres', value = genres)
                                                                                        embed.add_field(name = 'Themes', value = themes)
                                                                                        embed.add_field(name = 'Demographics', value = demographics)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                                    embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = trailer_image)
                                                                                embed.add_field(name = 'Background', value = background, inline = False)
                                                                                embed.add_field(name = 'Info', value = f'Episodes: {episodes}\nDuration {duration}\nYear Released: {released_year}\nBroadcasts: {broadcast}\nSource: {source}\nStatus: {status}\nAiring: {airing}\nAired: {aired}')
                                                                                embed.add_field(name = 'Trailer', value = trailer_url, inline = False)
                                                                                embed.add_field(name = 'Genres', value = genres)
                                                                                embed.add_field(name = 'Themes', value = themes)
                                                                                embed.add_field(name = 'Demographics', value = demographics)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                        await interaction.response.send_message(embed = embed, ephemeral = True)
                                                                @discord.ui.button(
                                                                    label = '>',
                                                                    style = discord.ButtonStyle.green
                                                                    )
                                                                async def nb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                                    if interaction.user.id == ctx.user.id:
                                                                        if self.current_page < 3:
                                                                            self.current_page += 1
                                                                        if self.current_page == 2:
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            trailer_url = data['trailer']['url']
                                                                            trailer_image = data['trailer']['images']['image_url']
                                                                            title_english = data['title_english']
                                                                            title_japanese = data['title_japanese']
                                                                            background = data['background']
                                                                            source = data['source']
                                                                            episodes = data['episodes']
                                                                            status = data['status']
                                                                            airing = data['airing']
                                                                            aired = data['aired']['string']
                                                                            duration = data['duration']
                                                                            released_year = data['year']
                                                                            broadcast = data['broadcast']['string']
                                                                            genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                            themes = ' | '.join([theme['name'] for theme in data['themes']])
                                                                            demographics = ' | '.join([demographic['name'] for demographic in data['demographics']])
                                                                            if trailer_url == 'null':
                                                                                trailer_url = 'None'
                                                                            if trailer_image == 'null':
                                                                                trailer_image = data['images']['jpg']['image_url']
                                                                            if background == '':
                                                                                background = 'None'
                                                                            if genres == '':
                                                                                genres = 'None'
                                                                            if themes == '':
                                                                                themes = 'None'
                                                                            if demographics == '':
                                                                                demographics = 'None'
                                                                            rating = data['rating']
                                                                            if rating == 'Rx - Hentai':
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            title = f'{title_english} | {title_japanese}',
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                        embed.set_thumbnail(url = trailer_image)
                                                                                        embed.add_field(name = 'Background', value = background, inline = False)
                                                                                        embed.add_field(name = 'Info', value = f'Episodes: {episodes}\nDuration {duration}\nYear Released: {released_year}\nBroadcasts: {broadcast}\nSource: {source}\nStatus: {status}\nAiring: {airing}\nAired: {aired}')
                                                                                        embed.add_field(name = 'Trailer', value = trailer_url, inline = False)
                                                                                        embed.add_field(name = 'Genres', value = genres)
                                                                                        embed.add_field(name = 'Themes', value = themes)
                                                                                        embed.add_field(name = 'Demographics', value = demographics)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                                    embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = trailer_image)
                                                                                embed.add_field(name = 'Background', value = background, inline = False)
                                                                                embed.add_field(name = 'Info', value = f'Episodes: {episodes}\nDuration {duration}\nYear Released: {released_year}\nBroadcasts: {broadcast}\nSource: {source}\nStatus: {status}\nAiring: {airing}\nAired: {aired}')
                                                                                embed.add_field(name = 'Trailer', value = trailer_url, inline = False)
                                                                                embed.add_field(name = 'Genres', value = genres)
                                                                                embed.add_field(name = 'Themes', value = themes)
                                                                                embed.add_field(name = 'Demographics', value = demographics)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        elif self.current_page == 3:
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            image_url = data['images']['jpg']['image_url']
                                                                            producers = ' | '.join([producer['name'] for producer in data['producers']])
                                                                            licensors = ' | '.join([licensor['name'] for licensor in data['licensors']])
                                                                            studios = ' | '.join([stuido['name'] for stuido in data['studios']])
                                                                            if producers == '':
                                                                                producers = 'None'
                                                                            if licensors == '':
                                                                                licensors = 'None'
                                                                            if studios == '':
                                                                                studios = 'None'
                                                                            rating = data['rating']
                                                                            if rating == 'Rx - Hentai':
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                        embed.set_thumbnail(url = image_url)
                                                                                        embed.add_field(name = 'Producers', value = producers, inline = False)
                                                                                        embed.add_field(name = 'Licensors', value = licensors, inline = False)
                                                                                        embed.add_field(name = 'Studios', value = studios, inline = False)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                                    embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.add_field(name = 'Producers', value = producers, inline = False)
                                                                                embed.add_field(name = 'Licensors', value = licensors, inline = False)
                                                                                embed.add_field(name = 'Studios', value = studios, inline = False)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                        await interaction.response.send_message(embed = embed, ephemeral = True)
                                                                @discord.ui.button(
                                                                    label = '>>',
                                                                    style = discord.ButtonStyle.blurple
                                                                )
                                                                async def rb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                                    if interaction.user.id == ctx.user.id:
                                                                        if self.current_search_page < pagination - 1:
                                                                            self.current_search_page += 1
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            image_url = data['images']['jpg']['image_url']
                                                                            title_english = data['title_english']
                                                                            title_japanese = data['title_japanese']
                                                                            synopsis = data['synopsis']
                                                                            rating = data['rating']
                                                                            if rating == 'Rx - Hentai':
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            title = f'{title_english} | {title_japanese}',
                                                                                            description = synopsis,
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                        embed.set_thumbnail(url = image_url)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                                    embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        elif self.current_search_page == pagination - 1:
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            image_url = data['images']['jpg']['image_url']
                                                                            title_english = data['title_english']
                                                                            title_japanese = data['title_japanese']
                                                                            synopsis = data['synopsis']
                                                                            rating = data['rating']
                                                                            if rating == 'Rx - Hentai':
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            title = f'{title_english} | {title_japanese}',
                                                                                            description = synopsis,
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                        embed.set_thumbnail(url = image_url)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                                    embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                        await interaction.response.send_message(embed = embed, ephemeral = True)
                                                                @discord.ui.button(
                                                                    label = 'Search',
                                                                    style = discord.ButtonStyle.blurple
                                                                )
                                                                async def sb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                                    if interaction.user.id == ctx.user.id:
                                                                        embed = discord.Embed(
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Menu')
                                                                        embed.add_field(name = 'Anime', value = 'Search Anime based commands | Search seasonal, upcoming, and Anime', inline = False)
                                                                        embed.add_field(name = 'Manga', value = 'Search Manga based commands | Search for a Manga', inline = False)
                                                                        embed.add_field(name = 'Character', value = 'Search for a character | Search for a character', inline = False)
                                                                        await interaction.response.edit_message(embed = embed, view = search_menu())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                        await interaction.response.send_message(embed = embed, ephemeral = True)
                                                            embed = discord.Embed(
                                                                title = f'{title_english} | {title_japanese}',
                                                                description = synopsis,
                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                timestamp = interaction.created_at
                                                            )
                                                            embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                            embed.set_thumbnail(url = image_url)
                                                            embed.set_footer(text = f'Page: 1 | {random.choice(random_footer_text)}')
                                                            await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                        else:
                                                            embed = discord.Embed(
                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                timestamp = interaction.created_at
                                                            )
                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                            embed.add_field(name = 'Rating', value = rating, inline = False)
                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                            await interaction.response.edit_message(embed = embed, view = search_menu())
                                                    else:
                                                        embed = discord.Embed(
                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                            timestamp = interaction.created_at
                                                        )
                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                        embed.add_field(name = 'Rating', value = rating, inline = False)
                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                        await interaction.response.edit_message(embed = embed, view = search_menu())
                                                else:
                                                    class anime_pagination_system(discord.ui.View):
                                                        current_page = 1
                                                        current_search_page = 0
                                                        def __init__(self):
                                                            super().__init__(timeout = None)
                                                        @discord.ui.button(
                                                            label = '<<',
                                                            style = discord.ButtonStyle.blurple
                                                        )
                                                        async def lb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                            if interaction.user.id == ctx.user.id:
                                                                if self.current_search_page > 0:
                                                                    self.current_search_page -= 1
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    image_url = data['images']['jpg']['image_url']
                                                                    title_english = data['title_english']
                                                                    title_japanese = data['title_japanese']
                                                                    synopsis = data['synopsis']
                                                                    rating = data['rating']
                                                                    if rating == 'Rx - Hentai':
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                            embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            title = f'{title_english} | {title_japanese}',
                                                                            description = synopsis,
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                        embed.set_thumbnail(url = image_url)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                elif self.current_search_page == 0:
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    image_url = data['images']['jpg']['image_url']
                                                                    title_english = data['title_english']
                                                                    title_japanese = data['title_japanese']
                                                                    synopsis = data['synopsis']
                                                                    rating = data['rating']
                                                                    if rating == 'Rx - Hentai':
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                            embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            title = f'{title_english} | {title_japanese}',
                                                                            description = synopsis,
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                        embed.set_thumbnail(url = image_url)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                            else:
                                                                embed = discord.Embed(
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                await interaction.response.send_message(embed = embed, ephemeral = True)
                                                        @discord.ui.button(
                                                            label = '<',
                                                            style = discord.ButtonStyle.green
                                                        )
                                                        async def pb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                            if interaction.user.id == ctx.user.id:
                                                                if self.current_page > 1:
                                                                    self.current_page -= 1
                                                                if self.current_page == 1:
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    image_url = data['images']['jpg']['image_url']
                                                                    title_english = data['title_english']
                                                                    title_japanese = data['title_japanese']
                                                                    synopsis = data['synopsis']
                                                                    rating = data['rating']
                                                                    if rating == 'Rx - Hentai':
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                            embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            title = f'{title_english} | {title_japanese}',
                                                                            description = synopsis,
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                        embed.set_thumbnail(url = image_url)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                elif self.current_page == 2:
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    trailer_url = data['trailer']['url']
                                                                    trailer_image = data['trailer']['images']['image_url']
                                                                    title_english = data['title_english']
                                                                    title_japanese = data['title_japanese']
                                                                    background = data['background']
                                                                    source = data['source']
                                                                    episodes = data['episodes']
                                                                    status = data['status']
                                                                    airing = data['airing']
                                                                    aired = data['aired']['string']
                                                                    duration = data['duration']
                                                                    released_year = data['year']
                                                                    broadcast = data['broadcast']['string']
                                                                    genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                    themes = ' | '.join([theme['name'] for theme in data['themes']])
                                                                    demographics = ' | '.join([demographic['name'] for demographic in data['demographics']])
                                                                    if trailer_url == 'null':
                                                                        trailer_url = 'None'
                                                                    if trailer_image == 'null':
                                                                        trailer_image = data['images']['jpg']['image_url']
                                                                    if background == '':
                                                                        background = 'None'
                                                                    if genres == '':
                                                                        genres = 'None'
                                                                    if themes == '':
                                                                        themes = 'None'
                                                                    if demographics == '':
                                                                        demographics = 'None'
                                                                    rating = data['rating']
                                                                    if rating == 'Rx - Hentai':
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = trailer_image)
                                                                                embed.add_field(name = 'Background', value = background, inline = False)
                                                                                embed.add_field(name = 'Info', value = f'Episodes: {episodes}\nDuration {duration}\nYear Released: {released_year}\nBroadcasts: {broadcast}\nSource: {source}\nStatus: {status}\nAiring: {airing}\nAired: {aired}')
                                                                                embed.add_field(name = 'Trailer', value = trailer_url, inline = False)
                                                                                embed.add_field(name = 'Genres', value = genres)
                                                                                embed.add_field(name = 'Themes', value = themes)
                                                                                embed.add_field(name = 'Demographics', value = demographics)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                            embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            title = f'{title_english} | {title_japanese}',
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                        embed.set_thumbnail(url = trailer_image)
                                                                        embed.add_field(name = 'Background', value = background, inline = False)
                                                                        embed.add_field(name = 'Info', value = f'Episodes: {episodes}\nDuration {duration}\nYear Released: {released_year}\nBroadcasts: {broadcast}\nSource: {source}\nStatus: {status}\nAiring: {airing}\nAired: {aired}')
                                                                        embed.add_field(name = 'Trailer', value = trailer_url, inline = False)
                                                                        embed.add_field(name = 'Genres', value = genres)
                                                                        embed.add_field(name = 'Themes', value = themes)
                                                                        embed.add_field(name = 'Demographics', value = demographics)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                            else:
                                                                embed = discord.Embed(
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                await interaction.response.send_message(embed = embed, ephemeral = True)
                                                        @discord.ui.button(
                                                            label = '>',
                                                            style = discord.ButtonStyle.green
                                                            )
                                                        async def nb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                            if interaction.user.id == ctx.user.id:
                                                                if self.current_page < 3:
                                                                    self.current_page += 1
                                                                if self.current_page == 2:
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    trailer_url = data['trailer']['url']
                                                                    trailer_image = data['trailer']['images']['image_url']
                                                                    title_english = data['title_english']
                                                                    title_japanese = data['title_japanese']
                                                                    background = data['background']
                                                                    source = data['source']
                                                                    episodes = data['episodes']
                                                                    status = data['status']
                                                                    airing = data['airing']
                                                                    aired = data['aired']['string']
                                                                    duration = data['duration']
                                                                    released_year = data['year']
                                                                    broadcast = data['broadcast']['string']
                                                                    genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                    themes = ' | '.join([theme['name'] for theme in data['themes']])
                                                                    demographics = ' | '.join([demographic['name'] for demographic in data['demographics']])
                                                                    if trailer_url == 'null':
                                                                        trailer_url = 'None'
                                                                    if trailer_image == 'null':
                                                                        trailer_image = data['images']['jpg']['image_url']
                                                                    if background == '':
                                                                        background = 'None'
                                                                    if genres == '':
                                                                        genres = 'None'
                                                                    if themes == '':
                                                                        themes = 'None'
                                                                    if demographics == '':
                                                                        demographics = 'None'
                                                                    rating = data['rating']
                                                                    if rating == 'Rx - Hentai':
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = trailer_image)
                                                                                embed.add_field(name = 'Background', value = background, inline = False)
                                                                                embed.add_field(name = 'Info', value = f'Episodes: {episodes}\nDuration {duration}\nYear Released: {released_year}\nBroadcasts: {broadcast}\nSource: {source}\nStatus: {status}\nAiring: {airing}\nAired: {aired}')
                                                                                embed.add_field(name = 'Trailer', value = trailer_url, inline = False)
                                                                                embed.add_field(name = 'Genres', value = genres)
                                                                                embed.add_field(name = 'Themes', value = themes)
                                                                                embed.add_field(name = 'Demographics', value = demographics)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                            embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            title = f'{title_english} | {title_japanese}',
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                        embed.set_thumbnail(url = trailer_image)
                                                                        embed.add_field(name = 'Background', value = background, inline = False)
                                                                        embed.add_field(name = 'Info', value = f'Episodes: {episodes}\nDuration {duration}\nYear Released: {released_year}\nBroadcasts: {broadcast}\nSource: {source}\nStatus: {status}\nAiring: {airing}\nAired: {aired}')
                                                                        embed.add_field(name = 'Trailer', value = trailer_url, inline = False)
                                                                        embed.add_field(name = 'Genres', value = genres)
                                                                        embed.add_field(name = 'Themes', value = themes)
                                                                        embed.add_field(name = 'Demographics', value = demographics)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                elif self.current_page == 3:
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    image_url = data['images']['jpg']['image_url']
                                                                    producers = ' | '.join([producer['name'] for producer in data['producers']])
                                                                    licensors = ' | '.join([licensor['name'] for licensor in data['licensors']])
                                                                    studios = ' | '.join([stuido['name'] for stuido in data['studios']])
                                                                    if producers == '':
                                                                        producers = 'None'
                                                                    if licensors == '':
                                                                        licensors = 'None'
                                                                    if studios == '':
                                                                        studios = 'None'
                                                                    rating = data['rating']
                                                                    if rating == 'Rx - Hentai':
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.add_field(name = 'Producers', value = producers, inline = False)
                                                                                embed.add_field(name = 'Licensors', value = licensors, inline = False)
                                                                                embed.add_field(name = 'Studios', value = studios, inline = False)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                            embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                        embed.set_thumbnail(url = image_url)
                                                                        embed.add_field(name = 'Producers', value = producers, inline = False)
                                                                        embed.add_field(name = 'Licensors', value = licensors, inline = False)
                                                                        embed.add_field(name = 'Studios', value = studios, inline = False)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                            else:
                                                                embed = discord.Embed(
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                await interaction.response.send_message(embed = embed, ephemeral = True)
                                                        @discord.ui.button(
                                                            label = '>>',
                                                            style = discord.ButtonStyle.blurple
                                                        )
                                                        async def rb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                            if interaction.user.id == ctx.user.id:
                                                                if self.current_search_page < pagination - 1:
                                                                    self.current_search_page += 1
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    image_url = data['images']['jpg']['image_url']
                                                                    title_english = data['title_english']
                                                                    title_japanese = data['title_japanese']
                                                                    synopsis = data['synopsis']
                                                                    rating = data['rating']
                                                                    if rating == 'Rx - Hentai':
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                            embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            title = f'{title_english} | {title_japanese}',
                                                                            description = synopsis,
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                        embed.set_thumbnail(url = image_url)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                elif self.current_search_page == pagination - 1:
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    image_url = data['images']['jpg']['image_url']
                                                                    title_english = data['title_english']
                                                                    title_japanese = data['title_japanese']
                                                                    synopsis = data['synopsis']
                                                                    rating = data['rating']
                                                                    if rating == 'Rx - Hentai':
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Dms')
                                                                            embed.add_field(name = 'Rating', value = rating, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            title = f'{title_english} | {title_japanese}',
                                                                            description = synopsis,
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                                        embed.set_thumbnail(url = image_url)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                            else:
                                                                embed = discord.Embed(
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                await interaction.response.send_message(embed = embed, ephemeral = True)
                                                        @discord.ui.button(
                                                            label = 'Search',
                                                            style = discord.ButtonStyle.blurple
                                                        )
                                                        async def sb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                            if interaction.user.id == ctx.user.id:
                                                                embed = discord.Embed(
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Menu')
                                                                embed.add_field(name = 'Anime', value = 'Search Anime based commands | Search seasonal, upcoming, and Anime', inline = False)
                                                                embed.add_field(name = 'Manga', value = 'Search Manga based commands | Search for a Manga', inline = False)
                                                                embed.add_field(name = 'Character', value = 'Search for a character | Search for a character', inline = False)
                                                                await interaction.response.edit_message(embed = embed, view = search_menu())
                                                            else:
                                                                embed = discord.Embed(
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                await interaction.response.send_message(embed = embed, ephemeral = True)
                                                    embed = discord.Embed(
                                                        title = f'{title_english} | {title_japanese}',
                                                        description = synopsis,
                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                        timestamp = interaction.created_at
                                                    )
                                                    embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime {anime_name}')
                                                    embed.set_thumbnail(url = image_url)
                                                    embed.set_footer(text = f'Page: 1 | {random.choice(random_footer_text)}')
                                                    await interaction.response.edit_message(embed = embed, view = anime_pagination_system())
                                            else:
                                                embed = discord.Embed(
                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                    timestamp = interaction.created_at
                                                )
                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Anime | Search Anime Anime Not Found For: {anime_name}')
                                                embed.set_footer(text = random.choice(random_footer_text))
                                                await interaction.response.edit_message(embed = embed, view = search_menu())
                                        else:
                                            embed = discord.Embed(
                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                timestamp = interaction.created_at
                                            )
                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Look\'s like the API is down :c')
                                            embed.add_field(name = 'What do I do now?', value = 'Wait until the API is back up or go play Valorant LOL')
                                            embed.set_footer(text = random.choice(random_footer_text))
                                            await interaction.response.send_message(embed = embed, view = search_menu())
                        await interaction.response.send_modal(search_modal())
                    else:
                        embed = discord.Embed(
                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.send_message(embed = embed, ephemeral = True)  
                elif select.values[0] == 'm':
                    if interaction.user.id == ctx.user.id:
                        class search_modal(discord.ui.Modal, title = 'Search Modal'):
                            manga_name = discord.ui.TextInput(
                                label = 'Search',
                                placeholder = 'Manga Name',
                                required = True
                            )
                            async def on_submit(self, interaction: discord.Interaction):
                                manga_name = self.manga_name.value
                                urlapi = mangaapi + manga_name
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(urlapi) as resp:
                                        if resp.status == 200:
                                            jsondata = await resp.json()
                                            data = jsondata['data']
                                            if data:
                                                data = jsondata['data'][0]
                                                pagination = jsondata['pagination']['items']['count']
                                                image_url = data['images']['jpg']['image_url']
                                                title_english = data['title_english']
                                                title_japanese = data['title_japanese']
                                                synopsis = data['synopsis']
                                                genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                if 'Hentai' in genres:
                                                    if interaction.channel.guild:
                                                        if interaction.channel.nsfw:
                                                            class manga_pagination_system(discord.ui.View):
                                                                current_page = 1
                                                                current_search_page = 0
                                                                def __init__(self):
                                                                    super().__init__(timeout = None)
                                                                @discord.ui.button(
                                                                    label = '<<',
                                                                    style = discord.ButtonStyle.blurple
                                                                )
                                                                async def lb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                                    if interaction.user.id == ctx.user.id:
                                                                        if self.current_search_page > 0:
                                                                            self.current_search_page -= 1
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            image_url = data['images']['jpg']['image_url']
                                                                            title_english = data['title_english']
                                                                            title_japanese = data['title_japanese']
                                                                            synopsis = data['synopsis']
                                                                            genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                            if 'Hentai' in genres:
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            title = f'{title_english} | {title_japanese}',
                                                                                            description = synopsis,
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                        embed.set_thumbnail(url = image_url)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                                    embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        elif self.current_search_page == 0:
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            image_url = data['images']['jpg']['image_url']
                                                                            title_english = data['title_english']
                                                                            title_japanese = data['title_japanese']
                                                                            synopsis = data['synopsis']
                                                                            genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                            if 'Hentai' in genres:
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            title = f'{title_english} | {title_japanese}',
                                                                                            description = synopsis,
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                        embed.set_thumbnail(url = image_url)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                                    embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                        await interaction.response.send_message(embed = embed, ephemeral = True)
                                                                @discord.ui.button(
                                                                    label = '<',
                                                                    style = discord.ButtonStyle.green
                                                                )
                                                                async def pb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                                    if interaction.user.id == ctx.user.id:
                                                                        if self.current_page > 1:
                                                                            self.current_page -= 1
                                                                        if self.current_page == 1:
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            image_url = data['images']['jpg']['image_url']
                                                                            title_english = data['title_english']
                                                                            title_japanese = data['title_japanese']
                                                                            synopsis = data['synopsis']
                                                                            genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                            if 'Hentai' in genres:
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            title = f'{title_english} | {title_japanese}',
                                                                                            description = synopsis,
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                        embed.set_thumbnail(url = image_url)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                                    embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        elif self.current_page == 2:
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            image_url = data['images']['jpg']['image_url']
                                                                            title_english = data['title_english']
                                                                            title_japanese = data['title_japanese']
                                                                            background = data['background']
                                                                            chapters = data['chapters']
                                                                            volumes = data['volumes']                                                                    
                                                                            status = data['status']
                                                                            publishing = data['publishing']
                                                                            published = data['published']['string']
                                                                            serializations = ' | '.join([serialization['name'] for serialization in data['serializations']])
                                                                            genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                            themes = ' | '.join([theme['name'] for theme in data['themes']])
                                                                            demographics = ' | '.join([demographic['name'] for demographic in data['demographics']])
                                                                            if chapters == 'null':
                                                                                chapters = 'None'
                                                                            if volumes == 'null':
                                                                                volumes = 'None'
                                                                            if background == '':
                                                                                background = 'None'
                                                                            if serializations == '':
                                                                                serializations = 'None'
                                                                            if genres == '':
                                                                                genres = 'None'
                                                                            if themes == '':
                                                                                themes = 'None'
                                                                            if demographics == '':
                                                                                demographics = 'None'
                                                                            if 'Hentai' in genres:
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            title = f'{title_english} | {title_japanese}',
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                        embed.set_thumbnail(url = image_url)
                                                                                        embed.add_field(name = 'Background', value = background, inline = False)
                                                                                        embed.add_field(name = 'Info', value = f'Chapters: {chapters}\nVolumes: {volumes}\nStatus: {status}\nPublishing: {publishing}\nPublished: {published}')
                                                                                        embed.add_field(name = 'Genres', value = genres)
                                                                                        embed.add_field(name = 'Themes', value = themes)
                                                                                        embed.add_field(name = 'Demographics', value = demographics)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                                    embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.add_field(name = 'Background', value = background, inline = False)
                                                                                embed.add_field(name = 'Info', value = f'Chapters: {chapters}\nVolumes: {volumes}\nStatus: {status}\nPublishing: {publishing}\nPublished: {published}')
                                                                                embed.add_field(name = 'Genres', value = genres)
                                                                                embed.add_field(name = 'Themes', value = themes)
                                                                                embed.add_field(name = 'Demographics', value = demographics)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                        await interaction.response.send_message(embed = embed, ephemeral = True)
                                                                @discord.ui.button(
                                                                    label = '>',
                                                                    style = discord.ButtonStyle.green
                                                                    )
                                                                async def nb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                                    if interaction.user.id == ctx.user.id:
                                                                        if self.current_page < 3:
                                                                            self.current_page += 1
                                                                        if self.current_page == 2:
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            image_url = data['images']['jpg']['image_url']
                                                                            title_english = data['title_english']
                                                                            title_japanese = data['title_japanese']
                                                                            background = data['background']
                                                                            chapters = data['chapters']
                                                                            volumes = data['volumes']                                                                    
                                                                            status = data['status']
                                                                            publishing = data['publishing']
                                                                            published = data['published']['string']
                                                                            serializations = ' | '.join([serialization['name'] for serialization in data['serializations']])
                                                                            genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                            themes = ' | '.join([theme['name'] for theme in data['themes']])
                                                                            demographics = ' | '.join([demographic['name'] for demographic in data['demographics']])
                                                                            if chapters == 'null':
                                                                                chapters = 'None'
                                                                            if volumes == 'null':
                                                                                volumes = 'None'
                                                                            if background == '':
                                                                                background = 'None'
                                                                            if serializations == '':
                                                                                serializations = 'None'
                                                                            if genres == '':
                                                                                genres = 'None'
                                                                            if themes == '':
                                                                                themes = 'None'
                                                                            if demographics == '':
                                                                                demographics = 'None'
                                                                            if 'Hentai' in genres:
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            title = f'{title_english} | {title_japanese}',
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                        embed.set_thumbnail(url = image_url)
                                                                                        embed.add_field(name = 'Background', value = background, inline = False)
                                                                                        embed.add_field(name = 'Info', value = f'Chapters: {chapters}\nVolumes: {volumes}\nStatus: {status}\nPublishing: {publishing}\nPublished: {published}')
                                                                                        embed.add_field(name = 'Genres', value = genres)
                                                                                        embed.add_field(name = 'Themes', value = themes)
                                                                                        embed.add_field(name = 'Demographics', value = demographics)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                                    embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.add_field(name = 'Background', value = background, inline = False)
                                                                                embed.add_field(name = 'Info', value = f'Chapters: {chapters}\nVolumes: {volumes}\nStatus: {status}\nPublishing: {publishing}\nPublished: {published}')
                                                                                embed.add_field(name = 'Genres', value = genres)
                                                                                embed.add_field(name = 'Themes', value = themes)
                                                                                embed.add_field(name = 'Demographics', value = demographics)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        elif self.current_page == 3:
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            image_url = data['images']['jpg']['image_url']
                                                                            authors = ' | '.join([author['name'] for author in data['authors']])
                                                                            genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                            if 'Hentai' in genres:
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                        embed.set_thumbnail(url = image_url)
                                                                                        embed.add_field(name = 'Authors', value = authors, inline = False)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                                    embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.add_field(name = 'Authors', value = authors, inline = False)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                        await interaction.response.send_message(embed = embed, ephemeral = True)
                                                                @discord.ui.button(
                                                                    label = '>>',
                                                                    style = discord.ButtonStyle.blurple
                                                                )
                                                                async def rb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                                    if interaction.user.id == ctx.user.id:
                                                                        if self.current_search_page < pagination - 1:
                                                                            self.current_search_page += 1
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            image_url = data['images']['jpg']['image_url']
                                                                            title_english = data['title_english']
                                                                            title_japanese = data['title_japanese']
                                                                            synopsis = data['synopsis']
                                                                            genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                            if 'Hentai' in genres:
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            title = f'{title_english} | {title_japanese}',
                                                                                            description = synopsis,
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                        embed.set_thumbnail(url = image_url)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                                    embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        elif self.current_search_page == pagination - 1:
                                                                            data = jsondata['data'][self.current_search_page]
                                                                            image_url = data['images']['jpg']['image_url']
                                                                            title_english = data['title_english']
                                                                            title_japanese = data['title_japanese']
                                                                            synopsis = data['synopsis']
                                                                            genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                            if 'Hentai' in genres:
                                                                                if interaction.channel.guild:
                                                                                    if interaction.channel.nsfw:
                                                                                        embed = discord.Embed(
                                                                                            title = f'{title_english} | {title_japanese}',
                                                                                            description = synopsis,
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                        embed.set_thumbnail(url = image_url)
                                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                    else:
                                                                                        embed = discord.Embed(
                                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                            timestamp = interaction.created_at
                                                                                        )
                                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                        embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                                        await interaction.response.defer()
                                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                                else:
                                                                                    embed = discord.Embed(
                                                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                        timestamp = interaction.created_at
                                                                                    )
                                                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                                    embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                    embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                                    embed.set_footer(text = random.choice(random_footer_text))
                                                                                    await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                        await interaction.response.send_message(embed = embed, ephemeral = True)
                                                                @discord.ui.button(
                                                                    label = 'Search',
                                                                    style = discord.ButtonStyle.blurple
                                                                )
                                                                async def sb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                                    if interaction.user.id == ctx.user.id:
                                                                        embed = discord.Embed(
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Menu')
                                                                        embed.add_field(name = 'manga', value = 'Search manga based commands | Search seasonal, upcoming, and manga', inline = False)
                                                                        embed.add_field(name = 'Manga', value = 'Search Manga based commands | Search for a Manga', inline = False)
                                                                        embed.add_field(name = 'Character', value = 'Search for a character | Search for a character', inline = False)
                                                                        await interaction.response.edit_message(embed = embed, view = search_menu())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                                        await interaction.response.send_message(embed = embed, ephemeral = True)
                                                            embed = discord.Embed(
                                                                title = f'{title_english} | {title_japanese}',
                                                                description = synopsis,
                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                timestamp = interaction.created_at
                                                            )
                                                            embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                            embed.set_thumbnail(url = image_url)
                                                            embed.set_footer(text = f'Page: 1 | {random.choice(random_footer_text)}')
                                                            await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                        else:
                                                            embed = discord.Embed(
                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                timestamp = interaction.created_at
                                                            )
                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                            embed.add_field(name = 'Rating', value = genres, inline = False)
                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                            await interaction.response.edit_message(embed = embed, view = search_menu())
                                                    else:
                                                        embed = discord.Embed(
                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                            timestamp = interaction.created_at
                                                        )
                                                        embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                        embed.add_field(name = 'Rating', value = genres, inline = False)
                                                        embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                        embed.set_footer(text = random.choice(random_footer_text))
                                                        await interaction.response.edit_message(embed = embed, view = search_menu())
                                                else:
                                                    class manga_pagination_system(discord.ui.View):
                                                        current_page = 1
                                                        current_search_page = 0
                                                        def __init__(self):
                                                            super().__init__(timeout = None)
                                                        @discord.ui.button(
                                                            label = '<<',
                                                            style = discord.ButtonStyle.blurple
                                                        )
                                                        async def lb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                            if interaction.user.id == ctx.user.id:
                                                                if self.current_search_page > 0:
                                                                    self.current_search_page -= 1
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    image_url = data['images']['jpg']['image_url']
                                                                    title_english = data['title_english']
                                                                    title_japanese = data['title_japanese']
                                                                    synopsis = data['synopsis']
                                                                    genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                    if 'Hentai' in genres:
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                            embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            title = f'{title_english} | {title_japanese}',
                                                                            description = synopsis,
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                        embed.set_thumbnail(url = image_url)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                elif self.current_search_page == 0:
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    image_url = data['images']['jpg']['image_url']
                                                                    title_english = data['title_english']
                                                                    title_japanese = data['title_japanese']
                                                                    synopsis = data['synopsis']
                                                                    genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                    if 'Hentai' in genres:
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                            embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            title = f'{title_english} | {title_japanese}',
                                                                            description = synopsis,
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                        embed.set_thumbnail(url = image_url)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                            else:
                                                                embed = discord.Embed(
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                await interaction.response.send_message(embed = embed, ephemeral = True)
                                                        @discord.ui.button(
                                                            label = '<',
                                                            style = discord.ButtonStyle.green
                                                        )
                                                        async def pb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                            if interaction.user.id == ctx.user.id:
                                                                if self.current_page > 1:
                                                                    self.current_page -= 1
                                                                if self.current_page == 1:
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    image_url = data['images']['jpg']['image_url']
                                                                    title_english = data['title_english']
                                                                    title_japanese = data['title_japanese']
                                                                    synopsis = data['synopsis']
                                                                    genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                    if 'Hentai' in genres:
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                            embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            title = f'{title_english} | {title_japanese}',
                                                                            description = synopsis,
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                        embed.set_thumbnail(url = image_url)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                elif self.current_page == 2:
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    image_url = data['images']['jpg']['image_url']
                                                                    title_english = data['title_english']
                                                                    title_japanese = data['title_japanese']
                                                                    background = data['background']
                                                                    chapters = data['chapters']
                                                                    volumes = data['volumes']                                                                    
                                                                    status = data['status']
                                                                    publishing = data['publishing']
                                                                    published = data['published']['string']
                                                                    serializations = ' | '.join([serialization['name'] for serialization in data['serializations']])
                                                                    genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                    themes = ' | '.join([theme['name'] for theme in data['themes']])
                                                                    demographics = ' | '.join([demographic['name'] for demographic in data['demographics']])
                                                                    if chapters == 'null':
                                                                        chapters = 'None'
                                                                    if volumes == 'null':
                                                                        volumes = 'None'
                                                                    if background == '':
                                                                        background = 'None'
                                                                    if serializations == '':
                                                                        serializations = 'None'
                                                                    if genres == '':
                                                                        genres = 'None'
                                                                    if themes == '':
                                                                        themes = 'None'
                                                                    if demographics == '':
                                                                        demographics = 'None'
                                                                    if 'Hentai' in genres:
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.add_field(name = 'Background', value = background, inline = False)
                                                                                embed.add_field(name = 'Info', value = f'Chapters: {chapters}\nVolumes: {volumes}\nStatus: {status}\nPublishing: {publishing}\nPublished: {published}')
                                                                                embed.add_field(name = 'Genres', value = genres)
                                                                                embed.add_field(name = 'Themes', value = themes)
                                                                                embed.add_field(name = 'Demographics', value = demographics)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                            embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            title = f'{title_english} | {title_japanese}',
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                        embed.set_thumbnail(url = image_url)
                                                                        embed.add_field(name = 'Background', value = background, inline = False)
                                                                        embed.add_field(name = 'Info', value = f'Chapters: {chapters}\nVolumes: {volumes}\nStatus: {status}\nPublishing: {publishing}\nPublished: {published}')
                                                                        embed.add_field(name = 'Genres', value = genres)
                                                                        embed.add_field(name = 'Themes', value = themes)
                                                                        embed.add_field(name = 'Demographics', value = demographics)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                            else:
                                                                embed = discord.Embed(
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                await interaction.response.send_message(embed = embed, ephemeral = True)
                                                        @discord.ui.button(
                                                            label = '>',
                                                            style = discord.ButtonStyle.green
                                                            )
                                                        async def nb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                            if interaction.user.id == ctx.user.id:
                                                                if self.current_page < 3:
                                                                    self.current_page += 1
                                                                if self.current_page == 2:
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    image_url = data['images']['jpg']['image_url']
                                                                    title_english = data['title_english']
                                                                    title_japanese = data['title_japanese']
                                                                    background = data['background']
                                                                    chapters = data['chapters']
                                                                    volumes = data['volumes']                                                                    
                                                                    status = data['status']
                                                                    publishing = data['publishing']
                                                                    published = data['published']['string']
                                                                    serializations = ' | '.join([serialization['name'] for serialization in data['serializations']])
                                                                    genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                    themes = ' | '.join([theme['name'] for theme in data['themes']])
                                                                    demographics = ' | '.join([demographic['name'] for demographic in data['demographics']])
                                                                    if chapters == 'null':
                                                                        chapters = 'None'
                                                                    if volumes == 'null':
                                                                        volumes = 'None'
                                                                    if background == '':
                                                                        background = 'None'
                                                                    if serializations == '':
                                                                        serializations = 'None'
                                                                    if genres == '':
                                                                        genres = 'None'
                                                                    if themes == '':
                                                                        themes = 'None'
                                                                    if demographics == '':
                                                                        demographics = 'None'
                                                                    if 'Hentai' in genres:
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.add_field(name = 'Background', value = background, inline = False)
                                                                                embed.add_field(name = 'Info', value = f'Chapters: {chapters}\nVolumes: {volumes}\nStatus: {status}\nPublishing: {publishing}\nPublished: {published}')
                                                                                embed.add_field(name = 'Genres', value = genres)
                                                                                embed.add_field(name = 'Themes', value = themes)
                                                                                embed.add_field(name = 'Demographics', value = demographics)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                            embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            title = f'{title_english} | {title_japanese}',
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                        embed.set_thumbnail(url = image_url)
                                                                        embed.add_field(name = 'Background', value = background, inline = False)
                                                                        embed.add_field(name = 'Info', value = f'Chapters: {chapters}\nVolumes: {volumes}\nStatus: {status}\nPublishing: {publishing}\nPublished: {published}')
                                                                        embed.add_field(name = 'Genres', value = genres)
                                                                        embed.add_field(name = 'Themes', value = themes)
                                                                        embed.add_field(name = 'Demographics', value = demographics)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                elif self.current_page == 3:
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    image_url = data['images']['jpg']['image_url']
                                                                    authors = ' | '.join([author['name'] for author in data['authors']])
                                                                    genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                    if 'Hentai' in genres:
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.add_field(name = 'Authors', value = authors, inline = False)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                            embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                        embed.set_thumbnail(url = image_url)
                                                                        embed.add_field(name = 'Authors', value = authors, inline = False)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                            else:
                                                                embed = discord.Embed(
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                await interaction.response.send_message(embed = embed, ephemeral = True)
                                                        @discord.ui.button(
                                                            label = '>>',
                                                            style = discord.ButtonStyle.blurple
                                                        )
                                                        async def rb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                            if interaction.user.id == ctx.user.id:
                                                                if self.current_search_page < pagination - 1:
                                                                    self.current_search_page += 1
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    image_url = data['images']['jpg']['image_url']
                                                                    title_english = data['title_english']
                                                                    title_japanese = data['title_japanese']
                                                                    synopsis = data['synopsis']
                                                                    genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                    if 'Hentai' in genres:
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                            embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            title = f'{title_english} | {title_japanese}',
                                                                            description = synopsis,
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                        embed.set_thumbnail(url = image_url)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                                elif self.current_search_page == pagination - 1:
                                                                    data = jsondata['data'][self.current_search_page]
                                                                    image_url = data['images']['jpg']['image_url']
                                                                    title_english = data['title_english']
                                                                    title_japanese = data['title_japanese']
                                                                    synopsis = data['synopsis']
                                                                    genres = ' | '.join([genre['name'] for genre in data['genres']])
                                                                    if 'Hentai' in genres:
                                                                        if interaction.channel.guild:
                                                                            if interaction.channel.nsfw:
                                                                                embed = discord.Embed(
                                                                                    title = f'{title_english} | {title_japanese}',
                                                                                    description = synopsis,
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                                embed.set_thumbnail(url = image_url)
                                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                            else:
                                                                                embed = discord.Embed(
                                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                    timestamp = interaction.created_at
                                                                                )
                                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | SFW Channel')
                                                                                embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                                embed.add_field(name = 'What do I do now?', value = 'If you still want to see the manga use this command in a NSFW channel', inline = False)
                                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                                await interaction.response.defer()
                                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                                        else:
                                                                            embed = discord.Embed(
                                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                                timestamp = interaction.created_at
                                                                            )
                                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Manga | Dms')
                                                                            embed.add_field(name = 'Rating', value = genres, inline = False)
                                                                            embed.add_field(name = 'What do I do now?', value = 'If you still want to see the Anime use this command in a NSFW channel', inline = False)
                                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                                            await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                                                    else:
                                                                        embed = discord.Embed(
                                                                            title = f'{title_english} | {title_japanese}',
                                                                            description = synopsis,
                                                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                            timestamp = interaction.created_at
                                                                        )
                                                                        embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                                        embed.set_thumbnail(url = image_url)
                                                                        embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                        await interaction.response.defer()
                                                                        await interaction.edit_original_response(embed = embed, view = self)
                                                            else:
                                                                embed = discord.Embed(
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                await interaction.response.send_message(embed = embed, ephemeral = True)
                                                        @discord.ui.button(
                                                            label = 'Search',
                                                            style = discord.ButtonStyle.blurple
                                                        )
                                                        async def sb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                            if interaction.user.id == ctx.user.id:
                                                                embed = discord.Embed(
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Menu')
                                                                embed.add_field(name = 'manga', value = 'Search manga based commands | Search seasonal, upcoming, and manga', inline = False)
                                                                embed.add_field(name = 'Manga', value = 'Search Manga based commands | Search for a Manga', inline = False)
                                                                embed.add_field(name = 'Character', value = 'Search for a character | Search for a character', inline = False)
                                                                await interaction.response.edit_message(embed = embed, view = search_menu())
                                                            else:
                                                                embed = discord.Embed(
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                                                embed.set_footer(text = random.choice(random_footer_text))
                                                                await interaction.response.send_message(embed = embed, ephemeral = True)
                                                    embed = discord.Embed(
                                                        title = f'{title_english} | {title_japanese}',
                                                        description = synopsis,
                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                        timestamp = interaction.created_at
                                                    )
                                                    embed.set_author(icon_url = interaction.user.avatar, name = f'Manga | Search | {manga_name}')
                                                    embed.set_thumbnail(url = image_url)
                                                    embed.set_footer(text = f'Page: 1 | {random.choice(random_footer_text)}')
                                                    await interaction.response.edit_message(embed = embed, view = manga_pagination_system())
                                            else:
                                                embed = discord.Embed(
                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                    timestamp = interaction.created_at
                                                )
                                                embed.set_author(icon_url = interaction.user.avatar, name = f'manga | Search | manga Not Found For: {manga_name}')
                                                embed.set_footer(text = random.choice(random_footer_text))
                                                await interaction.response.edit_message(embed = embed, view = search_menu())
                                        else:
                                            embed = discord.Embed(
                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                timestamp = interaction.created_at
                                            )
                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Look\'s like the API is down :c')
                                            embed.add_field(name = 'What do I do now?', value = 'Wait until the API is back up or go play Valorant LOL')
                                            embed.set_footer(text = random.choice(random_footer_text))
                                            await interaction.response.send_message(embed = embed, view = search_menu())
                        await interaction.response.send_modal(search_modal())
                    else:
                        embed = discord.Embed(
                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = 'This command isn\'t yours')
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.send_message(embed = embed, ephemeral = True) 
                elif select.values[0] == 'c':
                    if interaction.user.id == ctx.user.id:
                        class search_modal(discord.ui.Modal, title = 'Search Modal'):
                            character_name = discord.ui.TextInput(
                                label = 'Search',
                                placeholder = 'Character Name',
                                required = True
                            )
                            async def on_submit(self, interaction: discord.Interaction):
                                character_name = self.character_name.value
                                urlapi = characterapi + character_name
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(urlapi) as resp:
                                        if resp.status == 200:
                                            jsondata = await resp.json()
                                            data = jsondata['data']
                                            if data:
                                                data = jsondata['data'][0]
                                                pagination = jsondata['pagination']['items']['count']
                                                image_url = data['images']['jpg']['image_url']
                                                name_english = data['name']
                                                name_kanji = data['name_kanji']
                                                nicknames = ' | '.join([nickname for nickname in data['nicknames']])
                                                about = data['about']
                                                class character_pagination_system(discord.ui.View):
                                                    current_search_page = 0
                                                    def __init__(self):
                                                        super().__init__(timeout = None)
                                                    @discord.ui.button(
                                                        label = '<<',
                                                        style = discord.ButtonStyle.blurple
                                                    )
                                                    async def lb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                        if interaction.user.id == ctx.user.id:
                                                            if self.current_search_page > 0:
                                                                self.current_search_page -= 1
                                                                data = jsondata['data'][self.current_search_page]
                                                                image_url = data['images']['jpg']['image_url']
                                                                name_english = data['name']
                                                                name_kanji = data['name_kanji']
                                                                nicknames = ' | '.join([nickname for nickname in data['nicknames']])
                                                                about = data['about']
                                                                embed = discord.Embed(
                                                                    title = f'{name_english} | {name_kanji}',
                                                                    description = about,
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Character | Search | {character_name}')
                                                                embed.set_thumbnail(url = image_url)
                                                                embed.add_field(name = 'Nicknames', value = nicknames)
                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                await interaction.response.defer()
                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                            elif self.current_search_page == 0:
                                                                data = jsondata['data'][self.current_search_page]
                                                                image_url = data['images']['jpg']['image_url']
                                                                name_english = data['name']
                                                                name_kanji = data['name_kanji']
                                                                nicknames = ' | '.join([nickname for nickname in data['nicknames']])
                                                                about = data['about']
                                                                embed = discord.Embed(
                                                                    title = f'{name_english} | {name_kanji}',
                                                                    description = about,
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Character | Search | {character_name}')
                                                                embed.set_thumbnail(url = image_url)
                                                                embed.add_field(name = 'Nicknames', value = nicknames)
                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                await interaction.response.defer()
                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                        else:
                                                            embed = discord.Embed(
                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                timestamp = interaction.created_at
                                                            )
                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'This command isn\'t yours')
                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                            await interaction.response.send_message(embed = embed, ephemeral = True) 
                                                    @discord.ui.button(
                                                        label = '>>',
                                                        style = discord.ButtonStyle.blurple
                                                    )
                                                    async def rb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                        if interaction.user.id == ctx.user.id:
                                                            if self.current_search_page < pagination - 1:
                                                                self.current_search_page += 1
                                                                data = jsondata['data'][self.current_search_page]
                                                                image_url = data['images']['jpg']['image_url']
                                                                name_english = data['name']
                                                                name_kanji = data['name_kanji']
                                                                nicknames = ' | '.join([nickname for nickname in data['nicknames']])
                                                                about = data['about']
                                                                embed = discord.Embed(
                                                                    title = f'{name_english} | {name_kanji}',
                                                                    description = about,
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Character | Search | {character_name}')
                                                                embed.set_thumbnail(url = image_url)
                                                                embed.add_field(name = 'Nicknames', value = nicknames)
                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                await interaction.response.defer()
                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                            elif self.current_search_page == pagination - 1:
                                                                data = jsondata['data'][self.current_search_page]
                                                                image_url = data['images']['jpg']['image_url']
                                                                name_english = data['name']
                                                                name_kanji = data['name_kanji']
                                                                nicknames = ' | '.join([nickname for nickname in data['nicknames']])
                                                                about = data['about']
                                                                embed = discord.Embed(
                                                                    title = f'{name_english} | {name_kanji}',
                                                                    description = about,
                                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                    timestamp = interaction.created_at
                                                                )
                                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Character | Search | {character_name}')
                                                                embed.set_thumbnail(url = image_url)
                                                                embed.add_field(name = 'Nicknames', value = nicknames)
                                                                embed.set_footer(text = f'Page: {self.current_search_page + 1} | {random.choice(random_footer_text)}')
                                                                await interaction.response.defer()
                                                                await interaction.edit_original_response(embed = embed, view = self)
                                                        else:
                                                            embed = discord.Embed(
                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                timestamp = interaction.created_at
                                                            )
                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'This command isn\'t yours')
                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                            await interaction.response.send_message(embed = embed, ephemeral = True) 
                                                    @discord.ui.button(
                                                        label = 'Search',
                                                        style = discord.ButtonStyle.blurple
                                                    )
                                                    async def sb(self, interaction: discord.Interaction, Button: discord.ui.Button):
                                                        if interaction.user.id == ctx.user.id:
                                                            embed = discord.Embed(
                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                timestamp = ctx.created_at
                                                            )
                                                            embed.set_author(icon_url = ctx.user.avatar, name = 'Search | Menu')
                                                            embed.add_field(name = 'Anime', value = 'Search for an Anime', inline = False)
                                                            embed.add_field(name = 'Manga', value = 'Search for a Manga', inline = False)
                                                            embed.add_field(name = 'Character', value = 'Search for a character', inline = False)
                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                            await interaction.response.edit_message(embed = embed, view = search_menu())
                                                        else:
                                                            embed = discord.Embed(
                                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                                timestamp = interaction.created_at
                                                            )
                                                            embed.set_author(icon_url = interaction.user.avatar, name = 'This command isn\'t yours')
                                                            embed.set_footer(text = random.choice(random_footer_text))
                                                            await interaction.response.send_message(embed = embed, ephemeral = True) 
                                                embed = discord.Embed(
                                                    title = f'{name_english} | {name_kanji}',
                                                    description = about,
                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                    timestamp = interaction.created_at
                                                )
                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Character | Search | {character_name}')
                                                embed.set_thumbnail(url = image_url)
                                                embed.add_field(name = 'Nicknames', value = nicknames)
                                                embed.set_footer(text = f'Page: 1 | {random.choice(random_footer_text)}')
                                                await interaction.response.edit_message(embed = embed, view = character_pagination_system())
                                            else:
                                                embed = discord.Embed(
                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                    timestamp = interaction.created_at
                                                )
                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Character | Search | Character Not Found For: {character_name}')
                                                embed.set_footer(text = random.choice(random_footer_text))
                                                await interaction.response.edit_message(embed = embed, view = search_menu())
                                        else:
                                            embed = discord.Embed(
                                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                timestamp = interaction.created_at
                                            )
                                            embed.set_author(icon_url = interaction.user.avatar, name = 'Look\'s like the API is down :c')
                                            embed.add_field(name = 'What do I do now?', value = 'Wait until the API is back up or go play Valorant LOL')
                                            embed.set_footer(text = random.choice(random_footer_text))
                                            await interaction.response.send_message(embed = embed, view = search_menu())
                    await interaction.response.send_modal(search_modal())
                else:
                    embed = discord.Embed(
                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                        timestamp = interaction.created_at
                    )
                    embed.set_author(icon_url = interaction.user.avatar, name = 'This command isn\'t yours')
                    embed.set_footer(text = random.choice(random_footer_text))
                    await interaction.response.send_message(embed = embed, ephemeral = True) 
        embed = discord.Embed(
            color = discord.Color.from_str(random.choice(randomstrcolor)),
            timestamp = ctx.created_at
        )
        embed.set_author(icon_url = ctx.user.avatar, name = 'Search | Menu')
        embed.add_field(name = 'Anime', value = 'Search for an Anime', inline = False)
        embed.add_field(name = 'Manga', value = 'Search for a Manga', inline = False)
        embed.add_field(name = 'Character', value = 'Search for a character', inline = False)
        embed.set_footer(text = random.choice(random_footer_text))
        await ctx.response.send_message(embed = embed, view = search_menu())
    @search.error
    async def search_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(
                color = discord.Color.from_str('#eee0ca'),
                timestamp = ctx.created_at
            )
            embed.set_author(icon_url = ctx.user.avatar, name = "This command is on cooldown")
            embed.add_field(name = 'Woah?!', value = 'This command has a HUGE cooldown as there are limitations with the API')
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
    await client.add_cog(SearchCog(client))