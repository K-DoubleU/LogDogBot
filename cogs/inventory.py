import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing

class Inventory(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(hidden=True)
  async def givesap(self, ctx, member: discord.Member=None):
    if(ctx.author.id != 332601516626280450): return

    if member:

      user = str(member.id)

      if("inv" not in db[user]):
        db[user]["inv"] = {}
        await ctx.send("Inventory created. Please try again.")
        return
      elif("sap" in db[user]["inv"]):
        db[user]["inv"]["sap"] += 1
      else:
        db[user]["inv"]["sap"] = 1

    else:
      
      user = str(ctx.author.id)

      if("sap" in db[user]["inv"]):
        db[user]["inv"]["sap"] += 1
      else:
        db[user]["inv"]["sap"] = 1

  
  @commands.command(aliases = ["bag", "items", "inv"], help = "Displays your inventory. Use '.help Inventory' for a list of inventory-related commands")
  async def inventory(self, ctx):

    emoji = {
      "coins" : str(discord.utils.get(self.bot.emojis, name='coins')),
      "sap" : str(discord.utils.get(self.bot.emojis, name='sap'))
    }
    
    try:

      user = str(ctx.author.id)
      author = str(ctx.author.name)

      if(user not in db):
        db[user] = {
          "bal":0,
          "bank":0,
          "inv":{}
        }
        
        await ctx.send("Account created. Please try again.")
        return
      
      if("inv" not in db[user]):
        db[user]["inv"] = {}
        
        await ctx.send("Inventory created. Please try again.")
        return

      embed = discord.Embed(
        title = author + "'s Inventory"
      )

      total = db[user]["bal"] + db[user]["bank"]

      embed.add_field(
        name = emoji["coins"],
        value = total
      )
      
      for item, amount in db[user]["inv"].items():

        item_name = "Unknown"
        
        if(item in emoji.keys()): 
          item_name = emoji[item]
          
        embed.add_field(
          name = item_name,
          value = amount
        )

      await ctx.send(embed=embed)
        
    
    except Exception as e:
      print(e)

def setup(bot):
  bot.add_cog(Inventory(bot))