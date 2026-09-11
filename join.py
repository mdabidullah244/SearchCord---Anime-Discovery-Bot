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

class JoinCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(
        name = 'join',
        description = 'Join The Offical Rose ~ Server!'
    )
    @app_commands.checks.cooldown(1, 5.0, key=lambda i:(i.user.id))
    async def join(self, ctx: commands.Context):
        embed = discord.Embed(
            color = discord.Color.from_str(random.choice(randomstrcolor)),
            timestamp = ctx.created_at
        )
        embed.set_author(icon_url = ctx.user.avatar, name = 'Join | Rose ~ Server')
        embed.add_field(name = 'Server Link', value = 'https://discord.gg/EDQD7G7WnE')
        embed.set_footer(text = random.choice(random_footer_text))
        await ctx.response.send_message(embed = embed)

    @join.error
    async def join_error(self, ctx: commands.Context, error: Exception):
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
    await client.add_cog(JoinCog(client))