import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing

class Misc(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(hidden=True)
  async def resetcd(self, ctx, member: discord.Member = None):
    
    user = str(ctx.author.id)
    
    if user != "332601516626280450": return
      
    print("working")

    if(member):

      ctx.author = member
      ctx.message.author = member

      for command in ctx.bot.commands:
        print("command found")
        if command.is_on_cooldown(ctx):
          print("reset succeeded")
          command.reset_cooldown(ctx)
      return
      
    else:
      for command in ctx.bot.commands:
        print("command found")
        if command.is_on_cooldown(ctx):
          print("reset succeeded")
          command.reset_cooldown(ctx)

  @commands.command(hidden=True)
  async def resetallcd(self,ctx):
    
    if str(ctx.author.id) != "332601516626280450": return
      
    guild = ctx.bot.get_guild(893266661698838538)
    
    for member in guild.members:
 
      ctx.author = member
      ctx.message.author = member

      for command in ctx.bot.commands:
        if command.is_on_cooldown(ctx):
          print("reset succeeded for " + member.name)
          command.reset_cooldown(ctx)

    embed = discord.Embed(
      title = "Cooldown Reset",
      description = "Cooldowns for ALL users have been reset!"
    )

    await ctx.send(embed=embed)

  
def setup(bot):
  bot.add_cog(Misc(bot))