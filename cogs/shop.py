import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing

class Shop(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(aliases = ["store", "market", "grandexchange", "ge"], help = "Displays the shop. Use '.help buy' for more info on making purchases from the shop")
  async def shop(self, ctx, arg=None):

    coins = str(discord.utils.get(self.bot.emojis, name='coins'))

    embed = discord.Embed(
      title = "Grand Exchange",
      description = "Welcome to the GE!"
    )
    embed.set_author(
      name = "Log Dog Bot",
      icon_url = self.bot.user.avatar_url
    )
    
    shop = [{"name":"Money Printer :printer:", "price":10000, "desc":f"GP printer that can \ngenerate 10 {coins} per hour"},
           {"name":"Placeholder :bank:", "price":10000, "desc":f"Nothing to see here"}]

    i = 1
    for item in shop:
      name = item["name"]
      price = item["price"]
      desc = item["desc"]
      
      embed.add_field(
        name = str(i) + ". " + name,
        value = f"**{price}** {coins}\n{desc}"
        
      )
      i += 1

    embed.set_image(url="https://i.imgur.com/6hZNUAd.jpg?1")
    await ctx.send(embed=embed)


  # BUY COMMAND
  @commands.command(aliases=["purchase"], help="Buy an item from the shop. Can use the item name or the item's number in the shop")
  async def buy(self, ctx, *args):
    
    coins = str(discord.utils.get(self.bot.emojis, name='coins'))
    
    user = str(ctx.author.id)

    # Here we get the total amount of money the user has
    total = int(db[user]["bal"] + db[user]["bank"])

    # Begin embed construction
    embed = discord.Embed(
      title = "Order Status"
    )
    
    try:
      print(args)
      # FIRST, let's just default to an error if they don't put an item to purchase
      if(str(args) == "()"):
        embed.add_field(
            name = "Purchase Error",
            value = "Use '.help buy' for proper usage of this command"
          )
        await ctx.send(embed=embed)
        return
        
      # If they put printer, then let's try to complete the purchase
      # We can account for people saying printer OR money printer, by combining the args
      arg = " ".join(args[:])

      # If they try to buy item 1:
      if(str(arg).lower() == "printer" or str(arg).lower() == "money printer" or str(arg).lower() == "1"):



        if("print" in db[user]):

          embed.add_field(
            name = "Purchase Failed",
            value = "You already own a printer!"
          )

          await ctx.send(embed=embed)
          return

        # We need to see if the user has enough money to make the purchase
        if(total < 10000):

          # If total is less than 10000, this purchase cannot be made
          embed.add_field(
            name = "Purchase Failed",
            value = "You do not have enough " + coins + " to make this purchase"
          )

        # If the user DOES have enough, then we will make the purchase
        else:
          # If the cost is higher than what the user has in balance, then we need to set bal to 0 and subtract the rest from bank
          if(total > db[user]["bal"]):

            remainder = 10000 - db[user]["bal"]
            db[user]["bal"] = 0
            db[user]["bank"] -= remainder

          # Otherwise, if they have enough in their balance, then we just pull all of it from balance
          else:
            db[user]["bal"] -= 10000
            
          # We need to set their printlvl to 10 now that they have the printer
          db[user]["print"] = 10


            
          # Now we let them know it was successful
          embed.add_field(
            name = "Purchase Successful",
            value = "You have purchased **Money Printer** for 10000 " + coins + "\nUse '**.printer**' to check your printer status"
          )

        await ctx.send(embed=embed)
        return
      else:
        embed.add_field(
            name = "Purchase Error",
            value = "Use '.help buy' for proper usage of this command"
          )
        await ctx.send(embed=embed)
        return
    except Exception as e:
        print(e)
  

def setup(bot):
  bot.add_cog(Shop(bot))