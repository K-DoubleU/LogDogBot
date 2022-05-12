import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing
import asyncio
from datetime import datetime


def numformat(num):
      num = float('{:.3g}'.format(num))
      magnitude = 0
      while abs(num) >= 1000:
          magnitude += 1
          num /= 1000.0
      return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


class Pvp(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def duel(self, ctx, member: discord.Member = None):

    print("duel executed")
    
def setup(bot):
  bot.add_cog(Pvp(bot))