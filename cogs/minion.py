import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing
import asyncio
from datetime import datetime

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

class Minion(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  # QUEST COMMAND
  @commands.command()
  @commands.cooldown(1, 1800, commands.BucketType.user)
  async def quest(self, ctx):
    print("executing quest")

    global itemlist
    
    emoji = {
      "coins" : str(discord.utils.get(self.bot.emojis, name='coins')),
      "coins5" : str(discord.utils.get(self.bot.emojis, name='coins5')),
      "sapphire" : str(discord.utils.get(self.bot.emojis, name='sapphire')),
      "minion" : str(discord.utils.get(self.bot.emojis, name='Fridge')),
      "ticket": ":tickets:"
    }
    user = str(ctx.author.id)

    try:

      # Need to do rng magic for each item
      coin_chance = random.randint(1,10)
      sap_chance = random.randint(1,10)

      coin_amount = 1
      sap_amount = 1

      # Generate coin reward
      if(coin_chance == 1):
        coin_amount = random.randint(70000,100000)
      elif(coin_chance <= 3):
        coin_amount = random.randint(50000,70000)
      elif(coin_chance <= 6 ):
        coin_amount = random.randint(30000,50000)
      else:
        coin_amount = random.randint(10000,30000)

      # Generate sapphire reward
      if(sap_chance == 1):
        sap_amount = random.randint(70,100)
      elif(sap_chance <= 3):
        sap_amount = random.randint(40,70)
      elif(sap_chance <= 6 ):
        sap_amount = random.randint(20,40)
      else:
        sap_amount = random.randint(10,20)
      
      time = 1800
      
      embed = discord.Embed(
        title = "Minion Quest"
      )

      embed.set_thumbnail(url="https://i.imgur.com/n21TKLp.png")

      embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)
      
      # First, perform a check for if the user has a Minion
      if("minion" not in db[user]):
        embed.add_field(
          name = ":x: Quest Error",
          value = "You do NOT have a minion! Purchase one in the Grand Exchange"
        )

        await ctx.send(embed=embed)
        return

      embed.add_field(
        name = ":white_check_mark: Quest Started",
        value = "Your " + emoji["minion"] + " will return in: " + str(int(time/60)) + " minutes"
      )
      
      await ctx.send(embed=embed)

      await asyncio.sleep(time)

      finishembed = discord.Embed(
        title = ":white_check_mark: Quest Complete",
        description = "Your " + emoji["minion"] + " has returned with the following: "
      )

      finishembed.add_field(
        name = emoji["coins"],
        value = str(coin_amount)
      )

      finishembed.add_field(
        name = emoji["sapphire"],
        value = str(sap_amount)
      )

      if("inv" not in db[user]):
        db[user]["inv"] = {}

      if("sapphire" not in db[user]["inv"]):
        db[user]["inv"]["sapphire"] = sap_amount
  
      else:
        sap_remainder = 0
        if((db[user]["inv"]["sapphire"] + sap_amount) > 999):
          
          sap_remainder = (db[user]["inv"]["sapphire"] + sap_amount) - 999
          remainder_value = sap_remainder * 420
          
          db[user]["inv"]["sapphire"] = 999
          db[user]["bank"] += remainder_value

          finishembed.add_field(
            name = "Note: ",
            value = "You've reached the maximum amount of sapphires.\n**" + str(sap_remainder) + "** " + emoji["sapphire"] + " have been converted to **" + str(remainder_value) + "** " + emoji["coins"],
            inline = False
          )
          
        else:
          
          db[user]["inv"]["sapphire"] += sap_amount

      finishembed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)
      
      finishembed.set_thumbnail(url="https://i.imgur.com/n21TKLp.png")

      await ctx.send(ctx.author.mention)
      await ctx.send(embed = finishembed)

      

      db[user]["bank"] += coin_amount
      
    except Exception as e:
      print(e)
      await ctx.send("Dissy fix the bot u fuckin idiot")
      
  @quest.error
  async def quest_cooldown(self, ctx, error):
      if isinstance(error, commands.CommandOnCooldown):
          minutes = round(error.retry_after / 60)

          if (error.retry_after > 60):
            
              embed = discord.Embed(
                  title=f":exclamation: Quest Already in Progress!",
                  description=f"Time Remaining: **{int(minutes)} minutes**")
            
          else:
            
              embed = discord.Embed(
                  title=f":exclamation: Quest Already in Progress!",
                  description=f"Time Remaining: **{int(error.retry_after)}** seconds"
              )
          embed.set_author(
              name = ctx.author.display_name,
              icon_url=ctx.author.avatar_url)

          embed.set_thumbnail(url="https://i.imgur.com/n21TKLp.png")
          await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Minion(bot))