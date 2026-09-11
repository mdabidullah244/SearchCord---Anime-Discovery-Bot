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

class SetUpProfileCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(
        name = 'set_up_profile',
        description = 'Set Up Your Profile'
    )
    @app_commands.checks.cooldown(1, 15.0, key=lambda i:(i.user.id))
    async def set_up_profile(self, ctx: commands.Context):
        username = ctx.user.name
        connection = sqlite3.connect('databases/profile_db.db')
        cursor = connection.cursor()
        cursor.execute('SELECT username FROM profile_db_info WHERE username = ?', (username,))
        data = cursor.fetchone()
        if data:
            embed = discord.Embed(
                color = discord.Color.from_str(random.choice(randomstrcolor)),
                timestamp = ctx.created_at
            )
            embed.set_author(icon_url = ctx.user.avatar, name = f'Profile | Profile Already Set Up | {username}')
            embed.set_footer(text = random.choice(random_footer_text))
            await ctx.response.send_message(embed = embed)
            connection.close()
        else:
            class set_up_profile_menu(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout = None)
                @discord.ui.button(
                    label = 'Set Up Profile',
                    style = discord.ButtonStyle.green
                )
                async def set_up_profile_button(self, interaction: discord.Interaction, Button: discord.ui.Button):
                    if interaction.user.id == ctx.user.id:
                        class set_up_profile_modal(discord.ui.Modal, title = 'Set Up Profile'):
                            profile_bio = discord.ui.TextInput(
                                label = 'Bio',
                                placeholder = 'Write something about yourself',
                                style = discord.TextStyle.paragraph,
                                required = True
                            )
                            profile_gender = discord.ui.TextInput(
                                label = 'Gender',
                                placeholder = 'Your gender',
                                required = True
                            )
                            profile_birthday = discord.ui.TextInput(
                                label = 'Birthday',
                                placeholder = 'Your birthday',
                                required = True
                            )
                            async def on_submit(self, interaction: discord.Interaction):
                                profile_bio = self.profile_bio.value
                                profile_gender = self.profile_gender.value
                                profile_birthday = self.profile_birthday.value
                                embed = discord.Embed(
                                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                                    timestamp = interaction.created_at
                                )
                                embed.set_author(icon_url = interaction.user.avatar, name = f"Profile | Set Up Complete | {username}")
                                embed.set_footer(text = random.choice(random_footer_text))
                                await interaction.response.edit_message(embed = embed, view = None)
                                cursor.execute('INSERT INTO profile_db_info (username, bio, gender, birthday) VALUES (?, ?, ?, ?)', (username, profile_bio, profile_gender, profile_birthday))
                                connection.commit()
                                connection.close()
                        await interaction.response.send_modal(set_up_profile_modal())
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
                        connection.close()
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
            embed.set_author(icon_url = ctx.user.avatar, name = f'Profile | Profile Not Set Up')
            embed.set_thumbnail(url = ctx.user.avatar)
            embed.set_footer(text = 'Set up ')
            await ctx.response.send_message(embed = embed, view = set_up_profile_menu())
    @set_up_profile.error
    async def set_up_profile_error(self, ctx: commands.Context, error: Exception):
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
    await client.add_cog(SetUpProfileCog(client))