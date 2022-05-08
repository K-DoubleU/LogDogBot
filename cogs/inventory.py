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
      elif("sapphire" in db[user]["inv"]):
        db[user]["inv"]["sapphire"] += 1
      else:
        db[user]["inv"]["sapphire"] = 1

    else:
      
      user = str(ctx.author.id)

      if("sapphire" in db[user]["inv"]):
        db[user]["inv"]["sapphire"] += 1
      else:
        db[user]["inv"]["sapphire"] = 1

  
  @commands.command(aliases = ["bag", "items", "inv"], help = "Displays your inventory. Use '.help Inventory' for a list of inventory-related commands")
  async def inventory(self, ctx):

    emoji = {
      "coins" : str(discord.utils.get(self.bot.emojis, name='coins')),
      "sapphire" : str(discord.utils.get(self.bot.emojis, name='sapphire'))
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

  # SELL COMMAND
  @commands.command(help = "Sell an item in your inventory. You can provide an amount to sell multiple.\nExample: '.sell sapphire'\nExample: '.sell sapphire 32'")
  async def sell(self, ctx, *args):

    emoji = {
      "coins" : str(discord.utils.get(self.bot.emojis, name='coins')),
      "sapphire" : str(discord.utils.get(self.bot.emojis, name='sapphire'))
    }

    itemlist = {
      "sapphire":420
    }

    user = str(ctx.author.id)
    
    try:

      embed = discord.Embed(
        title = "Order Status"
      )
      
      if("inv" not in db[user]):
        await ctx.send("No inventory to sell from")
        return

      # Respond if a item isn't specified by the user
      if(str(args) == "()" or len(args) > 2):
        embed.add_field(
            name = "Sell Error",
            value = "Use '.help sell' for proper usage of this command"
          )
        await ctx.send(embed=embed)
        return
      
      if(len(args) > 1):
        
        arg = str(args[0])
        amount = int(args[-1])
        
      else:
        
        arg = str(args[0])
        amount = 1
        
      print(arg)

      itemexist = False

      for x in itemlist.keys():
        if(arg in x):
          itemexist=True
          arg = x
      # First, we make sure the item they're trying to sell is actually an item in the list
      if(itemexist):

        # Also need to make sure the user has that item, and that amount
        if(arg not in db[user]["inv"]):
          embed.add_field(
            name = "Sell Error",
            value = "You do not have any " + emoji[arg] + " to sell!"
          )
          await ctx.send(embed=embed)
          return

        if(amount > db[user]["inv"][arg]):
          embed.add_field(
            name = "Sell Error",
            value = "You do not have " + str(amount) + " " + emoji[arg] + " to sell!"
          )
          await ctx.send(embed=embed)
          return
        
        # If it's gotten past this point, we should be good to sell
        profit = amount * itemlist[arg]
        
        embed.add_field(
          name = "Item(s) Sold Successfully",
          value = "Sold: " + str(amount) + " " + emoji[arg] + "\nProfit: " + str(profit) + " " + emoji["coins"]
        )

        db[user]["inv"][arg] -= amount
        db[user]["bal"] += profit

        if(db[user]["inv"][arg] == 0):
          print(str(db[user]["inv"][arg]))
          del db[user]["inv"][arg]
      else:
        embed.add_field(
            name = "Sell Error",
            value = "Use '.help sell' for proper usage of this command"
          )
        await ctx.send(embed=embed)
        return

      await ctx.send(embed=embed)
    
    except Exception as e:
      print(e)

def setup(bot):
  bot.add_cog(Inventory(bot))