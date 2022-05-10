import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing

# Global itemlist for populating the shop, and for purchasing from
itemlist = [
  {
    "name":["Printer", "printer"],
    "desc": "GP Printer that generates **100**gp/hour",
    "price": 10000,
    "max":1
  },
  {
    "name":["Sapphire", "sapphire"],
    "desc": "A blue gem. Wow. Amazing.",
    "price": 420,
    "max":999
  },
  {
    "name":["Fridge", "minion"],
    "desc": "A basic fridge minion. Can be sent on quests for loot.",
    "price": 420000,
    "max":1
  }
]

class Shop(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  # SHOP COMMAND
  @commands.command(aliases = ["store", "market", "grandexchange", "ge"], help = "Displays the shop. Use '.help buy' for more info on making purchases from the shop")
  async def shop(self, ctx, arg=None):

    global itemlist
    
    emoji = {
      "coins" : str(discord.utils.get(self.bot.emojis, name='coins')),
      "sapphire" : str(discord.utils.get(self.bot.emojis, name='sapphire')),
      "minion" : str(discord.utils.get(self.bot.emojis, name='Fridge')),
      "ticket": ":tickets:",
      "printer":":printer:"
    }

    embed = discord.Embed(
      title = "Grand Exchange",
      description = "Welcome to the GE!"
    )
    embed.set_author(
      name = "Log Dog Bot",
      icon_url = self.bot.user.avatar_url
    )

   
    for item in itemlist:
      name = item["name"][0]
      price = item["price"]
      desc = item["desc"]

      getemoji = item["name"][1]
      print(getemoji)
      print(itemlist.index(item))
      
      embed.add_field(
        name = emoji[getemoji] + " " + name,
        value = f"**{price}** " + emoji["coins"] + f"\n{desc}"
        
      )


    embed.set_footer(text = "Use `.buy [item]` to purchase an item")
    embed.set_image(url="https://i.imgur.com/6hZNUAd.jpg?1")
    await ctx.send(embed=embed)


  # BUY COMMAND
  @commands.command(aliases=["purchase"], help="Buy an item from the shop.\nExample: .buy printer\nExample: .buy sapphire 6")
  async def buy(self, ctx, *args):

    global itemlist
    
    emoji = {
      "sapphire" : str(discord.utils.get(self.bot.emojis, name='sapphire')),
      "minion" : str(discord.utils.get(self.bot.emojis, name='Fridge')),
      "printer":":printer:"
    }
    
    coins = str(discord.utils.get(self.bot.emojis, name='coins'))
    
    user = str(ctx.author.id)

    # Here we get the total amount of money the user has
    total = int(db[user]["bal"] + db[user]["bank"])

    # Begin embed construction
    embed = discord.Embed(
      title = "Order Status"
    )

    embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)
    
    try:
      print(args)
      # FIRST, let's just default to an error if they don't put an item to purchase
      if(str(args) == "()"):
        embed.add_field(
            name = ":x: Purchase Error",
            value = "Use '.help buy' for proper usage of this command"
          )
        await ctx.send(embed=embed)
        return
        
      # If they put printer, then let's try to complete the purchase
      # We can account for people saying printer OR money printer, by combining the args
      arg = args[0]
      amount = 1

      if(len(args) > 1):
        if(args[1] == "all"):
          amount = "all"
        else:
          amount = int(args[1])

      # Check to see if the argument provided is an existing item in the itemlist

      for item in itemlist:
        if(arg.lower() in item["name"][0].lower() or arg in item["name"][1].lower()):

          arg = item["name"][1]
          
          if(amount == "all"):
              amount = int(total / item["price"])

          if(total < item["price"] * amount):
            embed.add_field(
              name = ":x: Purchase Failed",
              value = "You do not have enough " + coins + " to make this purchase"
            )
            await ctx.send(embed=embed)
            return
            
          if(arg == "printer"):

            if("print" in db[user] or amount != 1):

              embed.add_field(
                name = ":x: Purchase Failed",
                value = "You cannot own more than **1** :printer:"
              )

              await ctx.send(embed=embed)
              return

          if(arg == "minion"):
            
            if("minion" in db[user] or amount != 1):

              embed.add_field(
                name = ":x: Purchase Failed",
                value = "You cannot own more than **1** " + emoji["minion"]
              )

              await ctx.send(embed=embed)
              return
              
          if(arg == "sapphire"):

            if("sapphire" in db[user]["inv"]):
              if(db[user]["inv"]["sapphire"] == 999):
                embed.add_field(
                  name = ":x: Purchase Failed",
                  value = "You cannot own more than **999** " + emoji["sapphire"]
                )

                await ctx.send(embed=embed)
                return
                
          # Else, purchase SUCCEEDS

          # Initialize remainder to 0, in case the value is not needed
          remainder = 0

          # We need to set their printlvl to 100 now that they have the printer
          if(arg == "printer"):
            
            db[user]["print"] = 100

          # If they buy sapphire(s)
          if(arg == "sapphire"):

            #if sapphire, we check to see if they have an inv
            if("inv" not in db[user]):

              # create inv if needed
              db[user]["inv"] = {
                "sapphire":0
              }

            # check if they already have sapphires or not
            if(item["name"][1] not in db[user]["inv"]):
              
              db[user]["inv"][item["name"][1]] = 0

            # Force to 999 max
            if((db[user]["inv"]["sapphire"] + amount) > 999):

              amount = 999 - db[user]["inv"]["sapphire"]
              
              db[user]["inv"]["sapphire"] = 999

            else:
              
              db[user]["inv"]["sapphire"] += amount

          # If they buy a minion...
          if(arg == "minion"):

            db[user]["minion"] = 1
            
          # Money handling done below
          
          if(item["price"] * amount > db[user]["bal"]):

            remainder = (item["price"] * amount) - db[user]["bal"]
            
            db[user]["bal"] = 0
            db[user]["bank"] -= remainder

        # Otherwise, if they have enough in their balance, then we just pull all of it from balance
          else:
            
            db[user]["bal"] -= item["price"] * amount
          
        # Now we let them know it was successful
          embed.add_field(
            name = ":white_check_mark: Purchase Successful",
            value = "You have purchased **" + str(amount) + " " + emoji[item["name"][1]] + "** for " + str(item["price"] * amount) + " " + coins
          )

          await ctx.send(embed=embed)
          return
          

      embed.add_field(
        name = ":x: Purchase Error",
        value = "This item is not available. Check .shop for items"
      )
      
      await ctx.send(embed=embed)
      
    except Exception as e:
      print(e)
      embed = discord.Embed(
                title=":x: Purchase Error :x:",
                description="Use '.help buy' for proper usage of this command")

      await ctx.send(embed=embed)
  

def setup(bot):
  bot.add_cog(Shop(bot))