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
  
  @commands.command(help="Gives you a daily reward\nCooldown: 24 hours")
  @commands.cooldown(1, 86400, commands.BucketType.user)
  async def daily(self, ctx):

    allowed_channels = [972259001062526976,
                         971845967483658260]
    if ctx.channel.id not in allowed_channels:
      await ctx.send("Wrong channel, dumbass")
      return
          
    emoji = {
      "coins" : str(discord.utils.get(self.bot.emojis, name='coins')),
      "sapphire" : str(discord.utils.get(self.bot.emojis, name='sapphire')),
      "ticket" : ":tickets:"
    }
    
    user = str(ctx.author.id)

    prize = random.randint(3000,7500)

    sap_chance = random.randint(1,10)
    ticket_chance = random.randint(1,3)

    if(user not in db):

      db[user] = {
        "bal":0,
        "bank":0,
        "inv":{}
      }

      embed = discord.Embed(
        title = "Account Established",
        description = "We have created an account for you. Please try again."
      )
      embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)

      ctx.command.reset_cooldown(ctx)
      await ctx.send(embed=embed)
      return

    if("inv" not in db[user]):

      db[user]["inv"] = {}
      
      embed = discord.Embed(
        title = "Inventory Created",
        description = "We have created an inventory for you. Please try again."
      )
      embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)

      ctx.command.reset_cooldown(ctx)
      await ctx.send(embed=embed)
      return
    
    embed = discord.Embed(
      title = "Daily Reward",
      description = "Here are your rewards for today's claim.\nMoney will go directly to your bank"
    )
    embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)

    embed.set_footer(text="You may claim again in 24 hours")

    embed.add_field(
      name = emoji["coins"],
      value = str(prize)
    )

    
    # Creating a list of item names for what we can get from daily
    prizepool = ["sapphire","ticket"]

    # Now to create a list of other rewards that we can loop through for the remaining output
    rewards = {}

    if(sap_chance == 1):
      rewards["sapphire"] = 7
    elif(sap_chance == 2):
      rewards["sapphire"] = 4
    elif(sap_chance == 3):
      rewards["sapphire"] = 3
    elif(sap_chance == 4):
      rewards["sapphire"] = 2
    else:
      rewards["sapphire"] = 1

    if(ticket_chance == 1):
      rewards["ticket"] = 1
    elif(ticket_chance == 2):
      rewards["ticket"] = 2
    else:
      rewards["ticket"] = 3

    # Now we have the amount of rewards won, so let's go ahead and loop through rewards and add each item to the output

    for reward in rewards.keys():
      embed.add_field(
        name = emoji[reward],
        value = str(rewards[reward])
      )

      # We need to check if the user has any of this item already existing or not
      if(reward in db[user]["inv"]):
        db[user]["inv"][reward] += rewards[reward]
      else:
        db[user]["inv"][reward] = rewards[reward]

    db[user]["bank"] += prize
    
    await ctx.send(embed=embed)
    
  
  @daily.error
  async def daily_cooldown(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      minutes = round(error.retry_after / 60)

      if(error.retry_after >= 3600):
        
        embed = discord.Embed(
          title=f":timer: Daily is on cooldown!",
          description=f"Try again in {int(minutes/60)} hours")
              
      elif (error.retry_after > 60):
              
        embed = discord.Embed(
          title=f":timer: Daily is on cooldown!",
          description=f"Try again in {int(minutes)} minutes")
              
      else:
              
        embed = discord.Embed(
          title=f":timer: Daily is on cooldown!",
          description=f"Try again in {int(error.retry_after)} seconds")

      embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)
      
      await ctx.send(embed=embed)
    else:
      print(error)
    

  
def setup(bot):
  bot.add_cog(Misc(bot))