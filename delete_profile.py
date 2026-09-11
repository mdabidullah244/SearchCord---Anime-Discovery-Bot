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

class DeleteProfileCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    @app_commands.command(
        name = 'delete_profile',
        description = 'Deletes Your Profile'
    )
    @app_commands.checks.cooldown(1, 15.0, key=lambda i:(i.user.id))
    async def delete_profile(self, ctx: commands.Context):
        username = ctx.user.name
        connection = sqlite3.connect('databases/profile_db.db')
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT username FROM profile_db_info WHERE username = ?', (username,))
            data = cursor.fetchone()
            if data:
                class delete_profile_menu(discord.ui.View):
                    def __init__(self):
                        super().__init__(timeout = None)
                    @discord.ui.button(
                        label = 'Profile',
                        style = discord.ButtonStyle.green
                    )
                    async def delete_profile_button(self, interaction: discord.Interaction, Button: discord.ui.Button):
                        if interaction.user.id == ctx.user.id:
                            embed = discord.Embed(
                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                timestamp = interaction.created_at
                            )
                            embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Profile Info Deleted')
                            embed.set_footer(text = random.choice(random_footer_text))
                            await interaction.response.edit_message(embed = embed, view = delete_profile_menu())
                            cursor.execute('DELETE FROM profile_db_info WHERE username = ?', (username,))
                            connection.commit()
                        else:
                            embed = discord.Embed(
                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                timestamp = interaction.created_at
                            )
                            embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                            embed.set_footer(text = random.choice(random_footer_text))
                            await interaction.response.send_message(embed = embed, ephemeral = True)
                    @discord.ui.button(
                        label = 'Anime',
                        style = discord.ButtonStyle.green
                    )
                    async def delete_anime_button(self, interaction: discord.Interaction, Button: discord.ui.Button):
                        if interaction.user.id == ctx.user.id:
                            embed = discord.Embed(
                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                timestamp = interaction.created_at
                            )
                            embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Anime Info Deleted')
                            embed.set_footer(text = random.choice(random_footer_text))
                            await interaction.response.edit_message(embed = embed, view = delete_profile_menu())
                            connection = sqlite3.connect('databases/profile_db_a.db')
                            cursor = connection.cursor()
                            cursor.execute('DELETE FROM profile_db_anime_info WHERE username = ?', (username,))
                            connection.commit()
                        else:
                            embed = discord.Embed(
                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                timestamp = interaction.created_at
                            )
                            embed.set_author(icon_url = interaction.user.avatar, name = "This command isn't yours")
                            embed.set_footer(text = random.choice(random_footer_text))
                            await interaction.response.send_message(embed = embed, ephemeral = True)
                    @discord.ui.button(
                        label = 'Manga',
                        style = discord.ButtonStyle.green
                    )
                    async def delete_manga_button(self, interaction: discord.Interaction, Button: discord.ui.Button):
                        if interaction.user.id == ctx.user.id:
                            embed = discord.Embed(
                                color = discord.Color.from_str(random.choice(randomstrcolor)),
                                timestamp = interaction.created_at
                            )
                            embed.set_author(icon_url = interaction.user.avatar, name = 'Profile | Manga Info Deleted')
                            embed.set_footer(text = random.choice(random_footer_text))
                            await interaction.response.edit_message(embed = embed, view = delete_profile_menu())
                            connection = sqlite3.connect('databases/profile_db_m.db')
                            cursor = connection.cursor()
                            cursor.execute('DELETE FROM profile_db_manga_info WHERE username = ?', (username,))
                            connection.commit()
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
                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                    timestamp = ctx.created_at
                )
                embed.set_author(icon_url = ctx.user.avatar, name = 'Profile | Delete Profile')
                embed.set_footer(text = random.choice(random_footer_text))
                await ctx.response.send_message(embed = embed, view = delete_profile_menu())
            else:
                embed = discord.Embed(
                    color = discord.Color.from_str(random.choice(randomstrcolor)),
                    timestamp = ctx.created_at
                )
                embed.set_author(icon_url = ctx.user.avatar, name = 'Profile | Profile Not Found')
                embed.set_footer(text = random.choice(random_footer_text))
                await ctx.response.send_message(embed = embed)
        finally:
            connection.close()
    @delete_profile.error
    async def delete_profile_error(self, ctx: commands.Context, error: Exception):
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
    await client.add_cog(DeleteProfileCog(client))
