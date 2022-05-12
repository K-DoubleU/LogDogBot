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

def numformat(num):
      num = float('{:.3g}'.format(num))
      magnitude = 0
      while abs(num) >= 1000:
          magnitude += 1
          num /= 1000.0
      return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

class Minion(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  # QUEST COMMAND
  @commands.command()
  @commands.cooldown(1, 3600, commands.BucketType.user)
  async def quest(self, ctx):
    print("executing quest")

    global itemlist
    
    emoji = {
      "coins" : str(discord.utils.get(self.bot.emojis, name='coins')),
      "coins5" : str(discord.utils.get(self.bot.emojis, name='coins5')),
      "sapphire" : str(discord.utils.get(self.bot.emojis, name='sapphire')),
      "minion" : str(discord.utils.get(self.bot.emojis, name='Fridge')),
      "ruby" : str(discord.utils.get(self.bot.emojis, name='ruby')),
      "ticket": ":tickets:"
    }
    user = str(ctx.author.id)

    try:

      # Need to do rng magic for each item
      coin_chance = random.randint(1,10)
      sap_chance = random.randint(1,10)
      ruby_chance = random.randint(1,10)

      coin_amount = 1
      sap_amount = 1
      ruby_amount = 1

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
        sap_amount = random.randint(30,40)
      else:
        sap_amount = random.randint(20,30)

      # Generate ruby reward
      if(ruby_chance == 1):
        ruby_amount = 5
      elif(ruby_chance <= 4):
        ruby_amount = 3
      else:
        ruby_amount = 1
      
      time = 3600
      
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
        value = "Your " + emoji["minion"] + " will return in: 1 hour"
      )
      
      await ctx.send(embed=embed)

      await asyncio.sleep(time)

      finishembed = discord.Embed(
        title = ":white_check_mark: Quest Complete",
        description = "Your " + emoji["minion"] + " has returned with the following: "
      )

      finishembed.add_field(
        name = emoji["coins"],
        value = str(numformat(coin_amount))
      )

      finishembed.add_field(
        name = emoji["sapphire"],
        value = str(sap_amount)
      )

      finishembed.add_field(
        name = emoji["ruby"],
        value = str(ruby_amount)
      )
      
      finishembed.set_footer(text="Money has been deposited to your bank")

      if("inv" not in db[user]):
        db[user]["inv"] = {}

      if("ruby" not in db[user]["inv"]):
        db[user]["inv"]["ruby"] = ruby_amount
      else:
        db[user]["inv"]["ruby"] += ruby_amount

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
            value = "You've reached the maximum amount of sapphires.\n**" + str(sap_remainder) + "** " + emoji["sapphire"] + " have been converted to **" + str(numformat(remainder_value)) + "** " + emoji["coins"],
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

  # ATTACK COMMAND
  @commands.command(help="Send your minion to attack another user. Has a chance to steal the user's gems.")
  @commands.cooldown(1, 1800, commands.BucketType.user)
  async def attack(self, ctx, member: discord.Member = None):

    user = str(ctx.author.id)

    global itemlist
    
    emoji = {
      "coins" : str(discord.utils.get(self.bot.emojis, name='coins')),
      "coins5" : str(discord.utils.get(self.bot.emojis, name='coins5')),
      "sapphire" : str(discord.utils.get(self.bot.emojis, name='sapphire')),
      "minion" : str(discord.utils.get(self.bot.emojis, name='Fridge')),
      "ruby" : str(discord.utils.get(self.bot.emojis, name='ruby')),
      "ticket": ":tickets:"
    }
    
    embed = discord.Embed(
      title = ":exclamation: Minion Attack"
    )

    try:
      
      if(user not in db):
        db[user] = {
          "bal":0,
          "bank":0
        }
        
      if("minion" not in db[user]):
        
        embed.add_field(
          name = ":x: Attack Error",
          value = "You do not have a minion!\nPurchase one in the Grand Exchange"
        )

        await ctx.send(embed=embed)
        ctx.command.reset_cooldown(ctx)
        return
        
      else:

        if(member):

          # Create user object for mentioned user
          person = str(member.id)
          
          loot_chance = random.randint(1,10)

          successchance = False
          
          if(loot_chance <= 5): 
            successchance = True
          # Calculate loot

          # Calculate sapphires
          sap_amount = 0

          if(person not in db):

            embed.add_field(
              name = ":x: Attack Error",
              value = "User to attack not found"
            )
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
            return
          
          if("inv" in db[person]):

            if("sapphire" in db[person]["inv"]):

              # We need to calculate chance for success
              if(successchance == True):
                
                embed.add_field(
                  name = ":white_check_mark: Attack Successful",
                  value = emoji["minion"] + " attacked " + member.name + "\n**Loot:**",
                  inline = False
                )
  
                # If they have sapphires, we want to take some
                sap_amount = random.randint(7,20)


              else:

                embed.add_field(
                  name = ":x: Attack Failed",
                  value = emoji["minion"] + " tried to attack " + member.name + ", but failed",
                  inline = False
                )
                
  
            else:
  
              embed.add_field(
                name = ":x: Attack Failed",
                value = "This user has 0 sapphires to loot!"
              )
              
              await ctx.send(embed=embed)
              ctx.command.reset_cooldown(ctx)
              return
              

          # Need to check for inv
          if("inv" not in db[user]):
            db[user]["inv"] = {}
          
          # Will only add sapphires to message if they took some
          if(sap_amount > 0):

            if(sap_amount > db[person]["inv"]["sapphire"]): 
              sap_amount = db[person]["inv"]["sapphire"]
            
            embed.add_field(
              name = emoji["sapphire"],
              value = str(sap_amount)
            )
              
          sap_remainder = 0


          if("sapphire" not in db[user]["inv"]):
            db[user]["inv"]["sapphire"] = 0

          # If they looted sapphires, let's check for max value
          if((db[user]["inv"]["sapphire"] + sap_amount) > 999):
            
            sap_remainder = (db[user]["inv"]["sapphire"] + sap_amount) - 999
            remainder_value = sap_remainder * 420
            
            db[user]["inv"]["sapphire"] = 999
            db[user]["bank"] += remainder_value
  
            embed.add_field(
              name = "Note: ",
              value = "You've reached the maximum amount of sapphires.\n**" + str(sap_remainder) + "** " + emoji["sapphire"] + " have been converted to **" + str(remainder_value) + "** " + emoji["coins"],
              inline = False
            )

          # If max value condition doesn't apply we just add the amount
          else:
            
            db[user]["inv"]["sapphire"] += sap_amount

          # In either case, we want to subtract sap_amount from the other person
          db[person]["inv"]["sapphire"] -= sap_amount
        
        else:

          embed.add_field(
            name = ":x: Attack Error",
            value = "You need to mention a user to attack!"
          )
          
          await ctx.send(embed=embed)
          
          ctx.command.reset_cooldown(ctx)
          
          return
  
      await ctx.send(embed=embed)
      
    except Exception as e:

      embed = discord.Embed(
        title = ":exclamation: Minion Attack"
      )
      embed.add_field(
        name = ":x: Attack Error",
        value = "Use '.help attack' for proper usage of this command"
      )
      await ctx.send(embed=embed)
      ctx.command.reset_cooldown(ctx)
      
      print(e)

  @attack.error
  async def attack_cooldown(self, ctx, error):
      if isinstance(error, commands.CommandOnCooldown):
        
          minutes = round(error.retry_after / 60)

          if (error.retry_after > 60):
            
              embed = discord.Embed(
                  title=f":timer: Attack on Cooldown!",
                  description=f"Try again in: **{int(minutes)} minutes**")
            
          else:
            
              embed = discord.Embed(
                  title=f":timer: Attack on Cooldown!",
                  description=f"Try again in: **{int(error.retry_after)}** seconds"
              )
          embed.set_author(
              name = ctx.author.display_name,
              icon_url=ctx.author.avatar_url)

          await ctx.send(embed=embed)
      else:
        embed = discord.Embed(
          title = ":exclamation: Minion Attack"
        )
        embed.add_field(
          name = ":x: Attack Error",
          value = "Use '.help attack' for proper usage of this command"
        )
        await ctx.send(embed=embed)
        ctx.command.reset_cooldown(ctx)

def setup(bot):
  bot.add_cog(Minion(bot))