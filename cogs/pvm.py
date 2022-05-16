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
  10 : 1154
}

def getlevel(exp):
  i = 0
  newlvl = 0
  for level, exp_amt in sorted(levels.items()):
    if(exp > exp_amt):
      i += 1
      newlvl += 1
    else:
      return newlvl

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

  @commands.command()
  async def resetxp(self, ctx, *args):

    if(args):
      return
    else:
      user = "332601516626280450"
      del db[user]["stats"]

      
  @commands.command()
  async def fight(self, ctx, arg = None):

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
      "hitpoints" : str(discord.utils.get(self.bot.emojis, name='hitpoints')),
      "skull" : str(discord.utils.get(self.bot.emojis, name='skull')),
      "bones" : str(discord.utils.get(self.bot.emojis, name='bones')),
      "ticket": ":tickets:"
    }

    enemies = {
      "goblin" : {
        "attack" : 1,
        "defense" : 1,
        "hp" : 5
      }
    }

    user = str(ctx.author.id)

    # If an argument isn't provided, display available enemies to fight
    if(not arg):

      embed = discord.Embed(
        title = "Available Enemies",
        description = "Use '.fight [enemy]'"
      )

      for mob, stats in enemies.items():

        embed.add_field(
          name = mob.capitalize() + emoji[mob],
          value = emoji["attack"] + " " + str(stats["attack"]) + "\n" + emoji["defense"] + " " + str(stats["defense"]) + "\n" + emoji["hitpoints"] + " " + str(stats["hp"])
        )

      await ctx.send(embed=embed)
      return

    if arg.lower() not in enemies:

      embed = discord.Embed(
        title = ":x: Combat Error",
        description = "Invalid Enemy"
      )

      embed.set_author(
        name = ctx.author.display_name,
        icon_url=ctx.author.avatar_url)

      await ctx.send(embed=embed)
      return
      
    # Build initial Embed
    embed = discord.Embed(
      title = emoji["combat"] + " In Combat"
    )
    
    embed.set_author(
        name = ctx.author.display_name,
        icon_url=ctx.author.avatar_url)

    if("stats" not in db[user]):
      db[user]["stats"] = {
        "attack" : 3,
        "defense" : 1,
        "hp" : 5
      }

    # Get player initial lvl
    print(getlevel(db[user]["stats"]["attack"]))

    initial_atk = getlevel(db[user]["stats"]["attack"])
    initial_def = getlevel(db[user]["stats"]["defense"])
    
    # Setup hp values for fight
    player_hp = db[user]["stats"]["hp"]
    enemy_hp = enemies["goblin"]["hp"]

    embed.add_field(
      name = ctx.author.name + "\n" + emoji["player"],
      value = emoji["hp"] * player_hp
    )

    embed.add_field(
      name = "Goblin" + "\n" + emoji["goblin"],
      value = emoji["hp"] * enemies["goblin"]["hp"]
    )

    msg = await ctx.send(embed=embed)

    enemy_empty = 0
    player_empty = 0
    
    while player_hp != 0 and enemy_hp != 0:

      playerhit = random.randint(0, getlevel(db[user]["stats"]["attack"]))
      enemyhit = random.randint(0, getlevel(enemies["goblin"]["attack"]))

      if(playerhit >= enemies["goblin"]["defense"] and enemy_hp > 0):

        enemy_hp -= 1
        enemy_empty += 1

        embed.remove_field(index=1)
        embed.insert_field_at(index=1, 
          name = "Goblin" + "\n" + emoji["goblin"] + emoji["hitsplash1"],
          value = (emoji["hp"] * enemy_hp) + (emoji["emptyhp"] * enemy_empty)
        )

      else:
        embed.remove_field(index=1)
        embed.insert_field_at(index=1, 
          name = "Goblin" + "\n" + emoji["goblin"] + emoji["zerosplash"],
          value = (emoji["hp"] * enemy_hp) + (emoji["emptyhp"] * enemy_empty)
        )

      if(enemyhit >= db[user]["stats"]["defense"] and player_hp > 0):

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

      result_embed = discord.Embed(
        title = ":white_check_mark: Battle Won!"
      )

      # Add experience
      attack_gained = random.randint(15,25)
      defense_gained = random.randint(15,25)

      db[user]["stats"]["attack"] += attack_gained
      db[user]["stats"]["defense"] += defense_gained

      result_embed.add_field(
        name = "XP Gained:",
        value = emoji["attack"] + " " + str(attack_gained) + "\n" + emoji["defense"] + " " + str(defense_gained)
      )

      newatk = getlevel(db[user]["stats"]["attack"])
      newdef = getlevel(db[user]["stats"]["defense"])

      # Add Loot

      if("inv" not in db[user]):
        db[user]["inv"] = {
          "bones" : 1
        }

      elif("bones" not in db[user]["inv"]):
        db[user]["inv"]["bones"] = 1

      else:
        db[user]["inv"]["bones"] += 1

      result_embed.add_field(
        name = "Loot:",
        value = emoji["bones"] + " 1",
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

    else:

      result_embed = discord.Embed(
        title = emoji["skull"] + " Battle Lost!"
      )

    result_embed.set_author(
        name = ctx.author.display_name,
        icon_url=ctx.author.avatar_url)

    await ctx.send(embed = result_embed)

    
def setup(bot):
  bot.add_cog(Pvm(bot))