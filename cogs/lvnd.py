import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing

class Lvnd(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.command()
  async def lvnd(self, ctx):

    lvnd_msgs = [
      "You're actually trash bro how are you so bad like wtf wow holy shit",
      "Stop being terrible, PLEASSEE just actually stop",
      "Ayo you're such a pussy ass bitch lmao",
      "Bro you built like a spoon like frfr",
      "Dumbass",
      "Bruh actually get shit on",
      "Cranking 90's on your boofy ass rn",
      "Open your ears you deaf motherfucker"
    ]

    randmsg = random.randint(0, len(lvnd_msgs)-1)
    
    await ctx.message.delete()
    await ctx.send("<@184515221300183040> " + lvnd_msgs[randmsg])

def setup(bot):
  bot.add_cog(Lvnd(bot))