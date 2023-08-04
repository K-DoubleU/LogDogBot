import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing
import asyncio
from datetime import datetime


levels = {
  1 : 0,
  2 : 83,
  3 : 174,
  4 : 276,
  5 : 388,
  6 : 512,
  7 : 650,
  8 : 801,
  9 : 969,
  10 : 1154,
  11 : 1358,
  12 : 1584,
  13 : 1833,
  14 : 2107,
  15 : 2411,
  16 : 2746,
  17 : 3115,
  18 : 3523,
  19 : 3973,
  20 : 4470,
  21 : 5018,
  22 : 5624,
  23 : 6291,
  24 : 7028,
  25 : 7842,
  26 : 8740,
  27 : 9730,
  28 : 10824,
  29 : 12031,
  30 : 13363,
  34 : 20224,
  35 : 22406,
  36 : 24815,
  37 : 27473,
  38 : 30408,
  39 : 33648,
  40 : 37224,
  41 : 41171,
  42 : 45529,
  43 : 50339,
  44 : 55649,
  45 : 61512,
  46 : 67983,
  47 : 75127,
  48 : 83014,
  49 : 91721,
  50 : 101333
}

hplevels = {
  5 : 0,
  6 : 300,
  7 : 1200,
  8 : 4800,
  9 : 19200,
  10 : 76800
}

def gethp(exp):
  i = 0
  newlvl = 4
  for level, exp_amt in sorted(hplevels.items()):
    if(exp >= exp_amt):
      i += 1
      newlvl = level
  return newlvl

def getlevel(exp):
  i = 0
  newlvl = 0
  for level, exp_amt in sorted(levels.items()):
    if(exp >= exp_amt):
      i += 1
      newlvl = level
  return newlvl

def getcombatlvl(user):
  combat_total = getlevel(db[user]["stats"]["attack"]) + getlevel(db[user]["stats"]["defense"]) + gethp(db[user]["stats"]["hp"])
  combat_lvl = combat_total/3
  return round(combat_lvl, 1)

def numformat(num):
      num = float('{:.3g}'.format(num))
      magnitude = 0
      while abs(num) >= 1000:
          magnitude += 1
          num /= 1000.0
      return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


class Pvm(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(hidden=True)
  async def resetxp(self, ctx, *args):

    if(args):
      return
    else:
      user = "332601516626280450"
      del db[user]["stats"]

  @commands.command(hidden=True)
  async def setxp(self, ctx, arg):

    user = "332601516626280450"
    db[user]["stats"]["attack"] = int(arg)
    db[user]["stats"]["defense"] = int(arg)
    db[user]["stats"]["hp"] = int(arg)

  @commands.command()
  async def stats(self, ctx):

    emoji = {
      "combat" : str(discord.utils.get(self.bot.emojis, name='combat')),
      "hp" : str(discord.utils.get(self.bot.emojis, name='hp')),
      "attack" : str(discord.utils.get(self.bot.emojis, name='attack')),
      "defense" : str(discord.utils.get(self.bot.emojis, name='defense'))
    }

    user = str(ctx.author.id)

    # Build stat embed
    embed = discord.Embed(
      title = ctx.author.name + "'s Stats"
    )

    if("stats" not in db[user]):

      db[user]["stats"] = {
        "attack" : 0,
        "defense" : 0,
        "hp" : 0
      }

    # CORRECTING OLD HP VAALUE DELETE THIS SECTION AT SOME POINT
    if("hp" in db[user]["stats"]):

      if db[user]["stats"]["hp"] == 5:
        db[user]["stats"]["hp"] = 0

    # Loop through stats and add to embed

    for stat, exp in db[user]["stats"].items():

      if(stat == "hp"):

        embed.add_field(
          name = emoji[stat],
          value = gethp(exp)
        )

      else:
        embed.add_field(
          name = emoji[stat],
          value = getlevel(exp)
        )

    embed.add_field(
      name = emoji["combat"],
      value = str(getcombatlvl(user)),
      inline = False
    )
    
    embed.set_thumbnail(url="https://i.imgur.com/oAwDJ1H.png")
    
    embed.set_author(
        name = ctx.author.display_name,
        icon_url=ctx.author.avatar_url)
    
    await ctx.send(embed=embed)
      
  @commands.command(aliases = ["combat", "pvm"], help = "Pvm combat! Enemies give experience points and loot.\nUse '.fight' to view the list of available enemies.")
  @commands.cooldown(1, 1200, commands.BucketType.user)
  async def fight(self, ctx, *args):

    emoji = {
      "coins" : str(discord.utils.get(self.bot.emojis, name='coins')),
      "coins5" : str(discord.utils.get(self.bot.emojis, name='coins5')),
      "sapphire" : str(discord.utils.get(self.bot.emojis, name='sapphire')),
      "minion" : str(discord.utils.get(self.bot.emojis, name='Fridge')),
      "ruby" : str(discord.utils.get(self.bot.emojis, name='ruby')),
      "goblin" : str(discord.utils.get(self.bot.emojis, name='goblin')),
      "combat" : str(discord.utils.get(self.bot.emojis, name='combat')),
      "hp" : str(discord.utils.get(self.bot.emojis, name='hp')),
      "emptyhp" : str(discord.utils.get(self.bot.emojis, name='emptyhp')),
      "player" : str(discord.utils.get(self.bot.emojis, name='player')),
      "hitsplash1" : str(discord.utils.get(self.bot.emojis, name='hitsplash1')),
      "zerosplash" : str(discord.utils.get(self.bot.emojis, name='zerosplash')),
      "attack" : str(discord.utils.get(self.bot.emojis, name='attack')),
      "defense" : str(discord.utils.get(self.bot.emojis, name='defense')),
      "skull" : str(discord.utils.get(self.bot.emojis, name='skull')),
      "bones" : str(discord.utils.get(self.bot.emojis, name='bones')),
      "cow" : str(discord.utils.get(self.bot.emojis, name='cow')),
      "rat" : str(discord.utils.get(self.bot.emojis, name='rat')),
      "farmer" : str(discord.utils.get(self.bot.emojis, name='farmer')),
      "scorpion" : str(discord.utils.get(self.bot.emojis, name='scorpion')),
      "skeleton" : str(discord.utils.get(self.bot.emojis, name='skeleton')),
      "moss giant" : str(discord.utils.get(self.bot.emojis, name='mossgiant')),
      "ticket": ":tickets:"
    }

    enemies = {
      "rat" : {
        "attack" : 1,
        "defense" : 1,
        "hp" : 3,
        "gp" : random.randint(20,100),
        "type" : "both",
        "exp" : random.randint(10,14),
        "loot" : {"bones" : 1}
      },
      "goblin" : {
        "attack" : 2,
        "defense" : 1,
        "hp" : 4,
        "gp" : random.randint(450,940),
        "type" : "atk",
        "exp" : random.randint(15,25),
        "loot" : {"bones" : 1}
      },
      "cow" : {
        "attack" : 1,
        "defense" : 3,
        "hp" : 6,
        "gp" : random.randint(220,400),
        "type" : "def",
        "exp" : random.randint(15,25),
        "loot" : {"bones" : 1}
      },
      "farmer" : {
        "attack" : 3,
        "defense" : 4,
        "hp" : 5,
        "gp" : random.randint(1000,1700),
        "type" : "both",
        "exp" : random.randint(55,75),
        "loot" : {"bones" : 1}
      },
      "scorpion" : {
        "attack" : 8,
        "defense" : 6,
        "hp" : 4,
        "gp" : random.randint(3200,5700),
        "type" : "atk",
        "exp" : random.randint(80,100),
        "loot" : {"bones" : 1}
      },
      "skeleton" : {
        "attack" : 10,
        "defense" : 12,
        "hp" : 6,
        "gp" : random.randint(6500,10200),
        "type" : "def",
        "exp" : random.randint(110,130),
        "loot" : {"bones" : 1}
      },
      "moss giant" : {
        "attack" : 13,
        "defense" : 13,
        "hp" : 7,
        "gp" : random.randint(11000,16900),
        "type" : "both",
        "exp" : random.randint(250,290),
        "loot" : {"bones" : 1}
      }
    }

    user = str(ctx.author.id)

    # If an argument isn't provided, display available enemies to fight
    if(len(args) == 0):

      embed = discord.Embed(
        title = "Available Enemies",
        description = "Use '.fight [enemy]'"
      )

      for mob, stats in enemies.items():

        
        embed.add_field(
          name = mob.capitalize() + emoji[mob],
          value = emoji["combat"] + " " + str(round((stats["attack"] + stats["defense"] + stats["hp"])/3, 1))
        )

      await ctx.send(embed=embed)
      ctx.command.reset_cooldown(ctx)
      return

    arg = " ".join(args[:])

    if arg.lower() not in enemies:

      embed = discord.Embed(
        title = ":x: Combat Error",
        description = "Invalid Enemy"
      )

      embed.set_author(
        name = ctx.author.display_name,
        icon_url=ctx.author.avatar_url)

      await ctx.send(embed=embed)
      ctx.command.reset_cooldown(ctx)
      return

    if(user not in db):
      db[user] = {
        "bal" : 0,
        "bank" : 0,
      }

    arg = arg.lower()
    
    # Build initial Embed
    embed = discord.Embed(
      title = emoji["combat"] + " In Combat"
    )
    
    embed.set_author(
        name = ctx.author.display_name,
        icon_url=ctx.author.avatar_url)

    embed.set_footer(text="Battle in Progress...")

    if("stats" not in db[user]):
      db[user]["stats"] = {
        "attack" : 0,
        "defense" : 0,
        "hp" : 0
      }

    # CORRECTING OLD HP VAALUE DELETE THIS SECTION AT SOME POINT
    if("hp" in db[user]["stats"]):

      if db[user]["stats"]["hp"] == 5:
        db[user]["stats"]["hp"] = 0

    # Get player initial lvl
    print(getlevel(db[user]["stats"]["attack"]))

    initial_atk = getlevel(db[user]["stats"]["attack"])
    initial_def = getlevel(db[user]["stats"]["defense"])
    initial_hp = gethp(db[user]["stats"]["hp"])
    
    # Setup hp values for fight
    player_hp = gethp(db[user]["stats"]["hp"])
    enemy_hp = enemies[arg]["hp"]

    embed.add_field(
      name = ctx.author.name + "\n" + emoji["player"],
      value = emoji["hp"] * player_hp
    )

    embed.add_field(
      name = arg.capitalize() + "\n" + emoji[arg],
      value = emoji["hp"] * enemies[arg]["hp"]
    )

    msg = await ctx.send(embed=embed)

    enemy_empty = 0
    player_empty = 0
    
    while player_hp != 0 and enemy_hp != 0:

      playerhit = random.randint(0, getlevel(db[user]["stats"]["attack"]))
      enemyhit = random.randint(0, enemies[arg]["attack"])

      if(enemies[arg]["attack"] < getlevel(db[user]["stats"]["defense"])):

        enemyhit = random.randint(0, enemies[arg]["attack"] + 3)

      if(getlevel(db[user]["stats"]["attack"]) < enemies[arg]["defense"]):

        playerhit = random.randint(0, getlevel(db[user]["stats"]["attack"]) + 2)

      if(playerhit >= enemies[arg]["defense"] and enemy_hp > 0):

        enemy_hp -= 1
        enemy_empty += 1

        embed.remove_field(index=1)
        embed.insert_field_at(index=1, 
          name = arg.capitalize() + "\n" + emoji[arg] + emoji["hitsplash1"],
          value = (emoji["hp"] * enemy_hp) + (emoji["emptyhp"] * enemy_empty)
        )

      else:
        embed.remove_field(index=1)
        embed.insert_field_at(index=1, 
          name = arg.capitalize() + "\n" + emoji[arg] + emoji["zerosplash"],
          value = (emoji["hp"] * enemy_hp) + (emoji["emptyhp"] * enemy_empty)
        )

      if(enemyhit >= getlevel(db[user]["stats"]["defense"]) and player_hp > 0):

        player_hp -= 1
        player_empty += 1

        embed.remove_field(index=0)
        embed.insert_field_at(index=0, 
          name = ctx.author.name + "\n" + emoji["player"] + emoji["hitsplash1"],
          value = (emoji["hp"] * player_hp) + (emoji["emptyhp"] * player_empty)
        )

      else:

        embed.remove_field(index=0)
        embed.insert_field_at(index=0, 
          name = ctx.author.name + "\n" + emoji["player"] + emoji["zerosplash"],
          value = (emoji["hp"] * player_hp) + (emoji["emptyhp"] * player_empty)
        )

      await msg.edit(embed=embed)
      await asyncio.sleep(2)

    # When combat is over, test if player is still above 0 hp
    if(player_hp > 0):

      embed.remove_field(index=1)
      embed.insert_field_at(index=1, 
        name = arg.capitalize() + "\n" + emoji[arg],
        value = (emoji["hp"] * enemy_hp) + (emoji["emptyhp"] * enemy_empty)
      )

      embed.remove_field(index=0)
      embed.insert_field_at(index=0, 
        name = ctx.author.name + "\n" + emoji["player"],
        value = (emoji["hp"] * player_hp) + (emoji["emptyhp"] * player_empty)
      )
      
      embed.set_footer(text="Battle Finished")
      await msg.edit(embed=embed)

      result_embed = discord.Embed(
        title = ":white_check_mark: Battle Won!"
      )

      # Add experience
      attack_gained = 0
      defense_gained = 0
      hp_gained = 0
      
      if(enemies[arg]["type"] == "atk"):
        
        attack_gained = enemies[arg]["exp"]
        hp_gained = int(enemies[arg]["exp"]/5)

      elif(enemies[arg]["type"] == "def"):
        
        defense_gained = enemies[arg]["exp"]
        hp_gained = int(enemies[arg]["exp"]/5)

      else:

        attack_gained = int(enemies[arg]["exp"] / 2)
        defense_gained = int(enemies[arg]["exp"] / 2)
        hp_gained = int(enemies[arg]["exp"]/10)
        

      db[user]["stats"]["attack"] += attack_gained
      db[user]["stats"]["defense"] += defense_gained
      db[user]["stats"]["hp"] += hp_gained

      if(attack_gained == 0):

        result_embed.add_field(
          name = "XP Gained:",
          value = emoji["defense"] + " " + str(defense_gained) + "\n" + emoji["hp"] + " " + str(hp_gained)
        )

      elif(defense_gained == 0):

        result_embed.add_field(
          name = "XP Gained:",
          value = emoji["attack"] + " " + str(attack_gained) + "\n" + emoji["hp"] + " " + str(hp_gained)
        )

      else:

        result_embed.add_field(
          name = "XP Gained:",
          value = emoji["attack"] + " " + str(attack_gained) + "\n" + emoji["defense"] + " " + str(defense_gained) + "\n" + emoji["hp"] + " " + str(hp_gained)
        )

      newatk = getlevel(db[user]["stats"]["attack"])
      newdef = getlevel(db[user]["stats"]["defense"])
      newhp = gethp(db[user]["stats"]["hp"])

      # Add Loot & Money
        
      if("inv" not in db[user]):
        
        db[user]["inv"] = {}

      toadd = ""
      
      for i, qty in enemies[arg]["loot"].items():
        
        toadd += emoji[i] + str(qty) + "\n"

        if(i not in db[user]["inv"]):
          
          db[user]["inv"][i] = qty

        else:
          
          db[user]["inv"][i] += qty

        

      gp_gained = enemies[arg]["gp"]
      db[user]["bal"] += gp_gained

      result_embed.add_field(
        name = "Loot:",
        value = toadd + emoji["coins"] + " " + str(gp_gained),
        inline = False
      )


      if(newatk > initial_atk):

        result_embed.add_field(
          name = "Level Up!",
          value = "Your " + emoji["attack"] + " lvl has increased to " + str(newatk) + "!",
          inline = False
        )

      if(newdef > initial_def):

        result_embed.add_field(
          name = "Level Up!",
          value = "Your " + emoji["defense"] + " lvl has increased to " + str(newdef) + "!",
          inline = False
        )

      if(newhp > initial_hp):
        
        result_embed.add_field(
          name = "Level Up!",
          value = "Your " + emoji["hp"] + " lvl has increased to " + str(newhp) + "!",
          inline = False
        )

    else:

      result_embed = discord.Embed(
        title = emoji["skull"] + " Battle Lost!"
      )

    result_embed.set_author(
        name = ctx.author.display_name,
        icon_url=ctx.author.avatar_url)

    await ctx.send(embed = result_embed)


  @fight.error
  async def fight_cooldown(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      minutes = round(error.retry_after / 60)

      if (error.retry_after >= 60):
          embed = discord.Embed(
              title=f":timer: Combat is on cooldown!",
              description=f"Try again in {minutes} minutes.")

      else:
          embed = discord.Embed(
              title=f":timer: Combat is on cooldown!",
              description=f"Try again in {int(error.retry_after)} seconds"
          )

      embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)

      await ctx.send(embed=embed)
    else:
      print(error)

    
def setup(bot):
  bot.add_cog(Pvm(bot))