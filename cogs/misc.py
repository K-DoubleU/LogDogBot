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
  
class Misc(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def jrod(self,ctx):

    await ctx.message.delete()
    await ctx.send("<@235564731685928970> RBI")
    
  # LVND COMMAND
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

    
  # DAILY COMMAND  
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
    rewards = {
      "sapphire":{"amount":1,"max":999},
      "ticket":{"amount":1, "max":999}
    }

    if(sap_chance == 1):
      rewards["sapphire"]["amount"] = 7
    elif(sap_chance == 2):
      rewards["sapphire"]["amount"] = 4
    elif(sap_chance == 3):
      rewards["sapphire"]["amount"] = 3
    elif(sap_chance == 4):
      rewards["sapphire"]["amount"] = 2
    else:
      rewards["sapphire"]["amount"] = 1

    if(ticket_chance == 1):
      rewards["ticket"]["amount"] = 1
    elif(ticket_chance == 2):
      rewards["ticket"]["amount"] = 2
    else:
      rewards["ticket"]["amount"] = 3

    # Now we have the amount of rewards won, so let's go ahead and loop through rewards and add each item to the output

    for name, reward in rewards.items():

      # We need to check if the user has any of this item already existing or not
      if(name in db[user]["inv"]):
        
        print("got here")
        print("reward: " + name + "\nDetails: " + str(reward))
              
        # Need to make sure they won't go over max amount
        totalquantity = db[user]["inv"][name] + reward["amount"]
        print(totalquantity)
        
        print("problem with doing the addition if this doesnt show")
        
        if(totalquantity > reward["max"]):
          print("also got here")
          reward["amount"] = reward["max"] - db[user]["inv"][name]
          
          print(reward["amount"])

        print("got here wowow")
        
        db[user]["inv"][name] += reward["amount"]
        
      else:
        
        print("somehow got here?")
        
        db[user]["inv"][name] = reward["amount"]
      
      embed.add_field(
        name = emoji[name],
        value = str(numformat(reward["amount"]))
      )

    # Add gp to bank
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