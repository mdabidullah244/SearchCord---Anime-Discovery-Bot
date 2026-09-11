import random
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

class HelpCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(
        name = 'help',
        description = 'Shows You All Available Commands'
    )
    @app_commands.checks.cooldown(1, 5.0, key=lambda i:(i.user.id))
    async def help(self, ctx: commands.Context):
        class help_menu(discord.ui.View):
            options = [
                discord.SelectOption(label = 'Profile', value = 'pv', description = 'View Profile Help Info'),
                discord.SelectOption(label = 'Search', value = 'seav', description = 'View Search Help Info'),
                discord.SelectOption(label = 'Action', value = 'av', description = 'View Action Help Info'),
                discord.SelectOption(label = 'Settings', value = 'setv', description = 'View Setting Help Info')
            ]
            @discord.ui.select(
                placeholder = 'Help Menu',
                options = options
            )
            async def help_menu_selection(self, interaction: discord.Interaction, select):
                select.disabled = True
                if select.values[0] == 'pv':
                    if interaction.user.id == ctx.user.id:
                        embed = discord.Embed(
                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = 'Help | Profile Info')
                        embed.add_field(name = 'Profile', value = 'View Profile Info: /profile -username\n/profile SohanaPrettiestGirlAlive', inline = False)
                        embed.add_field(name = 'Set Up', value = 'Set Up Profile Info: /set_up_profile\nSet Up Anime Info: /set_up_anime\nSet Up Manga Info: /set_up_manga', inline = False)
                        embed.add_field(name = 'Update', value = 'Update Profile Info: /update_profile', inline = False)
                        embed.add_field(name = 'Delete', value = 'Delete Profile Info: /delete_profile', inline = False)
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.edit_message(embed = embed, view = help_menu())
                    else:
                        embed = discord.Embed(
                            color = discord.Color.from_str('#eee0ca'),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.send_message(embed = embed, ephemeral = True)
                elif select.values[0] == 'seav':
                    if interaction.user.id == ctx.user.id:
                        embed = discord.Embed(
                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = 'Help | Search Info')
                        embed.add_field(name = 'Anime', value = 'Search Anime: /search -anime_name\n/search My Hero Academia', inline = False)
                        embed.add_field(name = 'Manga', value = 'Search Manga: /search -manga_name\n/search Jojos Bizzare Adventure', inline = False)
                        embed.add_field(name = 'Character', value = 'Search Character: /search -character_name\n/search Luffy', inline = False)
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.edit_message(embed = embed, view = help_menu())
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
                        embed = discord.Embed(
                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = 'Help | Action Info')
                        embed.add_field(name = 'Action', value = 'Use An Action:\n/action -action_type -user\n/action hug SohanaPrettiestGirlAlive')
                        embed.add_field(name = 'Need More Help?', value = 'This command lets you perform an action on yourself or to another user!')
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.edit_message(embed = embed, view = help_menu())
                    else:
                        embed = discord.Embed(
                            color = discord.Color.from_str('#eee0ca'),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.send_message(embed = embed, ephemeral = True)

                elif select.values[0] == 'setv':
                    if interaction.user.id == ctx.user.id:
                        embed = discord.Embed(
                            color = discord.Color.from_str(random.choice(randomstrcolor)),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = 'Help | Settings Info')
                        embed.add_field(name = 'W.I.P', value = 'W.I.P', inline = False)
                        embed.add_field(name = 'More Setting Options Soon!', value = 'W.I.P', inline = False)
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.edit_message(embed = embed, view = help_menu())
                    else:
                        embed = discord.Embed(
                            color = discord.Color.from_str('#eee0ca'),
                            timestamp = interaction.created_at
                        )
                        embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                        embed.set_footer(text = random.choice(random_footer_text))
                        await interaction.response.send_message(embed = embed, ephemeral = True)
        embed = discord.Embed(
            color = discord.Color.from_str(random.choice(randomstrcolor)),
            timestamp = ctx.created_at
        )
        embed.set_author(icon_url = ctx.user.avatar, name = 'Help | Menu')
        embed.set_footer(text = random.choice(random_footer_text))
        await ctx.response.send_message(embed = embed, view = help_menu())
    @help.error
    async def help_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(
                color = discord.Color.from_str('#eee0ca'),
                timestamp = ctx.created_at
            )
            embed.set_author(icon_url = ctx.user.avatar, name = "This command is on cooldown")
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
    await client.add_cog(HelpCog(client))