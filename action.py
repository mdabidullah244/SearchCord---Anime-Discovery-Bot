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

api = 'https://nekos.best/api/v2/'

class ActionCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(
        name = 'action',
        description = 'Do something to another player or express how your feeling!'
    )
    @app_commands.checks.cooldown(1, 30.0, key=lambda i:(i.user.id))
    async def action(self, ctx: commands.Context, user: discord.Member = None):
        class action_menu(discord.ui.View):
            def __init__(self):
                super().__init__(timeout = None)
            
            @discord.ui.button(
                label = 'Solo',
                style = discord.ButtonStyle.blurple
            )
            async def solobutton(self, interaction: discord.Interaction, Button: discord.ui.Button):
                if interaction.user.id == ctx.user.id:
                    if user == None:
                        class solo_menu(discord.ui.View):
                            options = [
                                discord.SelectOption(label = 'Blush', value = 'blush', description = 'Blush?!'),
                                discord.SelectOption(label = 'Cry', value = 'cry', description = 'Cry?!'),
                                discord.SelectOption(label = 'Dance', value = 'dance', description = 'Dance?!'),
                                discord.SelectOption(label = 'Faceplam', value = 'facepalm', description = 'Faceplam?!'),
                                discord.SelectOption(label = 'Happy', value = 'happy', description = 'Happy?!'),
                                discord.SelectOption(label = 'Laugh', value = 'laugh', description = 'Laugh?!'),
                                discord.SelectOption(label = 'Lurk', value = 'lurk', description = 'Lurk?!'),
                                discord.SelectOption(label = 'Nod', value = 'nod', description = 'Nod?!'),
                                discord.SelectOption(label = 'Nom', value = 'nom', description = 'Nom?!'),
                                discord.SelectOption(label = 'Nope', value = 'nope', description = 'Nope?!'),
                                discord.SelectOption(label = 'Pout', value = 'pout', description = 'Pout?!'),
                                discord.SelectOption(label = 'Shrug', value = 'shrug', description = 'Shrug?!'),
                                discord.SelectOption(label = 'Sleep', value = 'sleep', description = 'Sleep?!'),
                                discord.SelectOption(label = 'Think', value = 'think', description = 'Think?!'),
                                discord.SelectOption(label = 'Thumbsup', value = 'thumbsup', description = 'Thumbsup?!'),
                                discord.SelectOption(label = 'Yawn', value = 'yawn', description = 'Yawn?!')
                            ]
                            @discord.ui.select(
                                placeholder = 'Action | Solo Menu',
                                options = options
                            )
                            async def solo_menu_selection(self, interaction: discord.Interaction, select):
                                select.disabled = True
                                selection = select.values[0]
                                if interaction.user.id == ctx.user.id:
                                    urlapi = api + selection
                                    async with aiohttp.ClientSession() as session:
                                        async with session.get(urlapi) as resp:
                                            if resp.status == 200:
                                                jsondata = await resp.json()
                                                anime = jsondata['results'][0]
                                                anime_name = anime['anime_name']
                                                anime_url = anime['url']
                                                embed = discord.Embed(
                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                    timestamp = interaction.created_at
                                                )
                                                embed.set_author(icon_url = interaction.user.avatar, name = f'Action | {str(selection).capitalize()}')
                                                embed.set_image(url = anime_url)
                                                embed.set_footer(text = f'Anime Name: {anime_name} | {random.choice(random_footer_text)}')
                                                await interaction.response.edit_message(embed = embed, view = None)
                                            else:
                                                embed = discord.Embed(
                                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                    timestamp = interaction.created_at
                                                )
                                                embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Error')
                                                embed.set_footer(text = f"Something isn't right, but we're looking into it! | {random.choice(random_footer_text)}")
                                                await interaction.response.edit_message(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                        timestamp = interaction.created_at
                                    )
                                    embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                    embed.set_footer(text = random.choice(random_footer_text))
                                    await interaction.response.send_message(embed = embed, ephemeral = True)
                        embed = discord.Embed(
                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = 'Action | Solo | Menu')
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.edit_message(embed = embed, view = solo_menu())
                    else:
                        embed = discord.Embed(
                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = 'Action | Solo | You entered a user while trying to access the solo menu :c')
                        embed.set_footer(text = f'If you want to use this command leave the user value empty! | {random.choice(random_footer_text)}')
                        await interaction.response.edit_message(embed = embed, view = None)
                else:
                    embed = discord.Embed(
                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                        timestamp = interaction.created_at
                    )
                    embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                    embed.set_footer(text = random.choice(random_footer_text))
                    await interaction.response.send_message(embed = embed, ephemeral = True)
            @discord.ui.button(
                label = 'Duo',
                style = discord.ButtonStyle.blurple
            )
            async def duobutton(self, interaction: discord.Interaction, Button: discord.ui.Button):
                if interaction.user.id == ctx.user.id:
                    if user == ctx.user:
                        embed = discord.Embed(
                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = "You can't use duo commands with yourself!")
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.edit_message(embed = embed, view = None)
                    else:
                        if not user == None:
                            class duo_menu(discord.ui.View):
                                options = [
                                    discord.SelectOption(label = 'Bite', value = 'bite', description = 'Bite?!'),
                                    discord.SelectOption(label = 'Cuddle', value = 'cuddle', description = 'Cuddle?!'),
                                    discord.SelectOption(label = 'Feed', value = 'feed', description = 'Feed?!'),
                                    discord.SelectOption(label = 'Handhold', value = 'handhold', description = 'Handhold?!'),
                                    discord.SelectOption(label = 'Handshake', value = 'handshake', description = 'Handshake?!'),
                                    discord.SelectOption(label = 'Highfive', value = 'highfive', description = 'Highfive?!'),
                                    discord.SelectOption(label = 'Hug', value = 'hug', description = 'Hug?!'),
                                    discord.SelectOption(label = 'Kick', value = 'kick', description = 'Kick?!'),
                                    discord.SelectOption(label = 'Kiss', value = 'kiss', description = 'Kiss?!'),
                                    discord.SelectOption(label = 'Pat', value = 'pat', description = 'Pat?!'),
                                    discord.SelectOption(label = 'Peck', value = 'peck', description = 'Peck?!'),
                                    discord.SelectOption(label = 'Poke', value = 'poke', description = 'Poke?!'),
                                    discord.SelectOption(label = 'Punch', value = 'punch', description = 'Punch?!'),
                                    discord.SelectOption(label = 'Shoot', value = 'shoot', description = 'Shoot?!'),
                                    discord.SelectOption(label = 'Slap', value = 'slap', description = 'Slap?!'),
                                    discord.SelectOption(label = 'Stare', value = 'stare', description = 'Stare?!'),
                                    discord.SelectOption(label = 'Tickle', value = 'tickle', description = 'Tickle?!'),
                                    discord.SelectOption(label = 'Wave', value = 'wave', description = 'Wave?!'),
                                    discord.SelectOption(label = 'Wink', value = 'wink', description = 'Wink?!'),
                                    discord.SelectOption(label = 'Yeet', value = 'yeet', description = 'Yeet?!')
                                ]
                                @discord.ui.select(
                                    placeholder = 'Action | Duo Menu',
                                    options = options
                                )
                                async def duo_menu_selection(self, interaction: discord.Interaction, select):
                                    select.disabled = True
                                    selection = select.values[0]
                                    if interaction.user.id == ctx.user.id:
                                        urlapi = api + selection
                                        async with aiohttp.ClientSession() as session:
                                            async with session.get(urlapi) as resp:
                                                if resp.status == 200:
                                                    jsondata = await resp.json()
                                                    anime = jsondata['results'][0]
                                                    anime_name = anime['anime_name']
                                                    anime_url = anime['url']
                                                    embed = discord.Embed(
                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                        timestamp = interaction.created_at
                                                    )
                                                    embed.set_author(icon_url = interaction.user.avatar, name = f'Action | {interaction.user.display_name} Used {str(selection).capitalize()} On {user.display_name}!')
                                                    embed.set_image(url = anime_url)
                                                    embed.set_footer(text = f'Anime Name: {anime_name} | {random.choice(random_footer_text)}')
                                                    await interaction.response.edit_message(embed = embed, view = None)
                                                else:
                                                    embed = discord.Embed(
                                                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                                                        timestamp = interaction.created_at
                                                    )
                                                    embed.set_author(icon_url = interaction.user.avatar, name = 'Search | Anime | Error')
                                                    embed.set_footer(text = f"Something isn't right, but we're looking into it! | {random.choice(random_footer_text)}")
                                                    await interaction.response.edit_message(embed = embed)
                                    else:
                                        embed = discord.Embed(
                                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                                            timestamp = interaction.created_at
                                        )
                                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                                        embed.set_footer(text = random.choice(random_footer_text))
                                        await interaction.response.send_message(embed = embed, ephemeral = True)
                        else:
                            embed = discord.Embed(
                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                timestamp = interaction.created_at
                            )
                            embed.set_author(icon_url = interaction.user.avatar, name = 'Action | Duo | You did not enter a user while trying to access the duo menu :c')
                            embed.set_footer(text = f'If you want to use this command enter a member in the user value! | {random.choice(random_footer_text)}')
                            await interaction.response.edit_message(embed = embed, view = None)
                    embed = discord.Embed(
                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                        timestamp = interaction.created_at
                    )
                    embed.set_author(icon_url = interaction.user.avatar, name = 'Action | Duo | Menu')
                    embed.set_footer(text = random.choice(random_footer_text))
                    await interaction.response.edit_message(embed = embed, view = duo_menu())
                else:
                    embed = discord.Embed(
                        color = discord.Color.from_str(random.choice(randomstrcolor)),
                        timestamp = interaction.created_at
                    )
                    embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                    embed.set_footer(text = random.choice(random_footer_text))
                    await interaction.response.send_message(embed = embed, ephemeral = True)
        embed = discord.Embed(
            color = discord.Color.from_str(random.choice(randomstrcolor)),
            timestamp = ctx.created_at
        )
        embed.set_author(icon_url = ctx.user.avatar, name = 'Action | Menu')
        embed.add_field(name = 'Solo', value = 'Most of these commands are showing how you feel and are limited to only one user')
        embed.add_field(name = 'Duo', value = 'All commands need another user so make sure you didn\'t leave the {user} value blank!')
        embed.set_footer(text = random.choice(random_footer_text))
        await ctx.response.send_message(embed = embed, view = action_menu())
    @action.error
    async def action_error(self, ctx: commands.Context, error: Exception):
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
    await client.add_cog(ActionCog(client))