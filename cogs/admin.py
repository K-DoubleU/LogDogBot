import discord
from discord.ext import commands
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing
import asyncio
from datetime import datetime

class Admin(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(hidden=True)
  async def geticon(self, ctx):
    icon_url = ctx.guild.icon_url
    await ctx.send(f"The icon url is: {icon_url}")

  @commands.command(hidden=True)
  async def getemoji(self, ctx, emoji: discord.Emoji):
    await ctx.send(emoji.url)

  @commands.Cog.listener()
  async def on_message(self, message):
    
    fridge = str(discord.utils.get(self.bot.emojis, name='Fridge'))
    gamba = str(discord.utils.get(self.bot.emojis, name='x0r6ztGiggle'))
    
    if("fridge" in message.content.lower()):
      await message.add_reaction(fridge)

    if("gamba" in message.content.lower()):
      await message.add_reaction(gamba)

    if self.bot.user.mentioned_in(message):
      await message.channel.send("DON'T PING ME MOTHERFUCKER")

  @commands.command(hidden=True)
  async def purge(self, ctx, arg = 1):

    allowedroles = [
      discord.utils.find(lambda r: r.name == 'CEO', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Board', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Bot Dev', ctx.message.guild.roles)
    ]

    allowed = False
    
    for role in ctx.author.roles:
      if(role in allowedroles):
        allowed = True

    if(allowed == False):
      await ctx.send("You do not have the required role(s) to use this command. Fuck off.")
      return

    await ctx.channel.purge(limit=arg)

  # DEV LOG COMMAND
  @commands.command(hidden=True)
  async def devlog(self, ctx):

    embed = discord.Embed(
      title = "Bot Development Log"
    )
    
    pins = await ctx.channel.pins()
    
    for i in reversed(pins):

      created = i.created_at
      
      embed.add_field(
        name = str(created.strftime("%m/%d/%Y, %H:%M:%S")),
        value = i.content,
        inline = False
      )

    print("Log sent")
    await ctx.message.delete()
    await ctx.send(embed=embed)

  @commands.command(hidden=True)
  async def tierlist(self,ctx):
    minions = ["Fridge", "x0Fridge", "doucheFridge", "BoobaFridge", "Fridgium", "FridgeOnABridge", "FridgeOnABridgeNearARidgeAndAlso", "FridgeChamp"]

    embed = discord.Embed(
      title = "Fridge Tier List"
    )
    for minion in minions:

      emoji = str(discord.utils.get(self.bot.emojis, name=minion))
      embed.add_field(
        name = str(minions.index(minion) + 1),
        value = emoji,
        inline = False
      )

    await ctx.message.delete()
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Admin(bot))