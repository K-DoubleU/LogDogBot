import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing


def numformat(num):
      num = float('{:.3g}'.format(num))
      magnitude = 0
      while abs(num) >= 1000:
          magnitude += 1
          num /= 1000.0
      return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

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


  # Inventory command
  @commands.command(aliases = ["bag", "items", "inv"], help = "Displays your inventory. Use '.help Inventory' for a list of inventory-related commands")
  async def inventory(self, ctx):

    emoji = {
      "coins" : str(discord.utils.get(self.bot.emojis, name='coins')),
      "coins5" : str(discord.utils.get(self.bot.emojis, name='coins5')),
      "sapphire" : str(discord.utils.get(self.bot.emojis, name='sapphire')),
      "minion" : str(discord.utils.get(self.bot.emojis, name='Fridge')),
      "ruby" : str(discord.utils.get(self.bot.emojis, name='ruby')),
      "bones" : str(discord.utils.get(self.bot.emojis, name='bones')),
      "ticket": ":tickets:"
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
      embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)

      embed.set_thumbnail(url="https://i.imgur.com/wMQYUZ5.png")

      total = db[user]["bal"] + db[user]["bank"]

      embed.add_field(
        name = emoji["coins"],
        value = numformat(total)
      )
      
      if("sap" in db[user]["inv"].keys()):
        del db[user]["inv"]["sap"]
        
      for item, amount in db[user]["inv"].items():

        item_name = "Unknown"
        
        if(item in emoji.keys()): 
          item_name = emoji[item]

        if(amount == 0): continue
          
        embed.add_field(
          name = item_name,
          value = numformat(amount)
        )

      if("print" in db[user]):

        embed.add_field(
          name = "Printer:",
          value = ":printer:  " + str(db[user]["print"]) + " " + emoji["coins5"] + "/hr.",
          inline = False
        )
        
      if("minion" in db[user]):

        embed.add_field(
          name = "Minion:",
          value = emoji["minion"] + "  Lvl " + str(db[user]["minion"]),
          inline = False
        )

      await ctx.send(embed=embed)
        
    
    except Exception as e:
      print(e)

  # SELL COMMAND
  @commands.command(help = "Sell an item in your inventory. You can provide an amount to sell multiple.\nExample: '.sell sapphire'\nExample: '.sell sapphire 32'")
  async def sell(self, ctx, *args):

    emoji = {
      "coins" : str(discord.utils.get(self.bot.emojis, name='coins')),
      "sapphire" : str(discord.utils.get(self.bot.emojis, name='sapphire')),
      "ruby" : str(discord.utils.get(self.bot.emojis, name='ruby')),
    }

    itemlist = {
      "sapphire":420,
      "ruby":1000
    }

    user = str(ctx.author.id)
    
    try:

      embed = discord.Embed(
        title = "Order Status"
      )

      embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)
      
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
        if(args[1] == "all"):
          amount = "all"
        else:
          amount = int(args[1])   
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

        if(amount == "all"):
          amount = db[user]["inv"][arg]

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
          value = "Sold: " + str(amount) + " " + emoji[arg] + "\nProfit: " + str(numformat(profit)) + " " + emoji["coins"]
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

  # USE COMMAND
  @commands.command(help = "Use an item in your inventory.\nExample: '.use ticket'")
  async def use(self, ctx, *args):

    emoji = {
      "coins" : str(discord.utils.get(self.bot.emojis, name='coins')),
      "sapphire" : str(discord.utils.get(self.bot.emojis, name='sapphire')),
      "ticket": ":tickets:"
    }

    # Dictionary of usable items
    itemlist = {
      "ticket":"All Cooldowns Reset"
    }

    user = str(ctx.author.id)
    
    try:

      embed = discord.Embed(
        title = ":white_check_mark: Item Used"
      )

      embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)
      
      if("inv" not in db[user]):
        await ctx.send("You do not have any usable items!")
        return

      # Respond if a item isn't specified by the user
      if(str(args) == "()"):
        embed = discord.Embed(
            title = ":x: Use Error",
            description = "Use '.help use' for proper usage of this command"
          )
        embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        return
      
      if(len(args) > 1):
        
        arg = "".join(args[:])
        print(arg)
        
        
      else:
        
        arg = str(args[0])
        
      print(arg)

      itemexist = False

      for x in itemlist.keys():
        if(x in arg):
          itemexist=True
          arg = x
          
      # First, we make sure the item they're trying to sell is actually an item in the list
      if(itemexist):

        # Also need to make sure the user has that item
        if(arg not in db[user]["inv"]):
          embed = discord.Embed(
            title = ":x: Use Error",
            description = "You do not have any " + emoji[arg] + " to use!"
          )
          embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)
          await ctx.send(embed=embed)
          return
        
        # If it's gotten past this point, we should be good to use
        
        embed.add_field(
          name = emoji[arg] + " Used Successfully",
          value = itemlist[arg]
        )

        db[user]["inv"][arg] -= 1

        if(arg == "ticket"):
          for command in ctx.bot.commands:
            print("command found")
            banned_cmds = ["daily", "quest"]
            if(command.is_on_cooldown(ctx) and command.name not in banned_cmds):
              print("reset succeeded")
              command.reset_cooldown(ctx)

        if(db[user]["inv"][arg] == 0):
          print(str(db[user]["inv"][arg]))
          del db[user]["inv"][arg]
      else:
        embed = discord.Embed(
            title = ":x: Use Error",
            description = "Use '.help use' for proper usage of this command"
          )
        embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        return

      await ctx.send(embed=embed)
    
    except Exception as e:
      print(e)

  # INFO COMMAND
  @commands.command(aliases=["view", "information", "details"],help = "View details of an item. Includes sell value and functionality when applicable.\nExample: '.info sapphire'")
  async def info(self, ctx, *args):

    emoji = {
      "coins" : str(discord.utils.get(self.bot.emojis, name='coins')),
      "sapphire" : str(discord.utils.get(self.bot.emojis, name='sapphire')),
      "ticket": ":tickets:",
      "fridge": str(discord.utils.get(self.bot.emojis, name='Fridge')),
      "ruby": str(discord.utils.get(self.bot.emojis, name='ruby')),
      "printer": ":printer:"
    }

    thumbnails = {
      "sapphire" : "https://i.imgur.com/kzH7sGv.png",
      "fridge" : "https://i.imgur.com/vDgZeTY.png",
      "printer" : "https://i.imgur.com/lU1suPR.png",
      "ticket" : "https://i.imgur.com/eFX2Z6h.png",
      "ruby" : "https://i.imgur.com/VAOY9KY.png"
    }

    # Dictionary of viewable items
    itemlist = {
      "ticket" : {
        "function":"Resets all cooldowns for the users",
        "price" : 0
      },
      "sapphire" : {
        "function":"A blue gem. Wow. Amazing.",
        "price":420
      },
      "fridge" : {
        "function":"A basic fridge minion. Can be sent on quests for loot.",
        "price":420000
      },
      "printer" : {
        "function" : "GP Printer that generates 100 gp per hour.",
        "price":10000
      },
      "ruby" : {
        "function" : "A red gem. Wow. Amazing. \nObtained from quests.",
        "price":1000
      }
    }

    user = str(ctx.author.id)
    
    try:

      embed = discord.Embed(
        title = ":mag: Item Info"
      )

      embed.set_author(name="Log Dog Bot", icon_url=ctx.bot.user.avatar_url)

      # Respond if a item isn't specified by the user
      if(str(args) == "()"):
        embed = discord.Embed(
            title = ":x: Info Error",
            description = "You must specify an item\nUse '.help info' for proper usage of this command"
          )
        embed.set_author(name="Log Dog Bot", icon_url=ctx.bot.user.avatar_url)
        await ctx.send(embed=embed)
        return
      
      if(len(args) > 1):
        
        arg = "".join(args[:])
        print(arg)
        
        
      else:
        
        arg = str(args[0])
        
      print(arg)

      itemexist = False

      for x in itemlist.keys():
        if(arg in x):
          itemexist=True
          arg = x
          
      # First, we make sure the item they're trying to sell is actually an item in the list
      if(itemexist):
        
        # If it's gotten past this point, we should be good to view

        item_details = "**Description:** " + str(itemlist[arg]["function"]) + "\n**Price:** " + str(numformat(itemlist[arg]["price"])) + " " + emoji["coins"]
        
        embed.add_field(
          name = emoji[arg],
          value = item_details
        )

        embed.set_thumbnail(
          url = thumbnails[arg]
        )
        
      else:

        embed.add_field(
          name = ":x: Unknown Item",
          value = arg + " is not a valid item"
        )

      await ctx.send(embed=embed)
    
    except Exception as e:
      print(e)

  #Placeholder for stats display message

def setup(bot):
  bot.add_cog(Inventory(bot))