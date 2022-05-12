import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing
import asyncio
from datetime import datetime

class Admin(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(hidden=True)
  async def geticon(self, ctx):
    icon_url = ctx.guild.icon_url
    await ctx.send(f"The icon url is: {icon_url}")

  @commands.command(hidden=True)
  async def getemoji(self, ctx, emoji: discord.Emoji):
    await ctx.send(emoji.url)

  @commands.Cog.listener()
  async def on_message(self, message):
    
    fridge = str(discord.utils.get(self.bot.emojis, name='Fridge'))
    gamba = str(discord.utils.get(self.bot.emojis, name='x0r6ztGiggle'))
    
    if("fridge" in message.content.lower()):
      await message.add_reaction(fridge)

    if("gamba" in message.content.lower()):
      await message.add_reaction(gamba)

    if self.bot.user.mentioned_in(message):
      await message.channel.send("DON'T PING ME MOTHERFUCKER")

  @commands.command(hidden=True)
  async def purge(self, ctx, arg = 1):

    allowedroles = [
      discord.utils.find(lambda r: r.name == 'CEO', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Board', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Bot Dev', ctx.message.guild.roles)
    ]

    allowed = False
    
    for role in ctx.author.roles:
      if(role in allowedroles):
        allowed = True

    if(allowed == False):
      await ctx.send("You do not have the required role(s) to use this command. Fuck off.")
      return

    await ctx.channel.purge(limit=arg)

  @commands.command(hidden=True)
  async def kill(self, ctx, member: discord.Member):

    if(ctx.author.id != 332601516626280450):
      await ctx.send("You do not have the required role(s) to use this command. Fuck off.")
      return

    embed = discord.Embed(
      title = "REST IN PIECE, BITCH"
    )
    
    if(member):

      user = str(member.id)
      
      if(user in db):
        embed.add_field(
          name = member.name,
          value = "ily im sorry I'm testing this pls don't hate me"
        )

        del db[user]

        await ctx.send(embed=embed)
      

  # DEV LOG COMMAND
  @commands.command(hidden=True)
  async def devlog(self, ctx):

    embed = discord.Embed(
      title = "Bot Development Log"
    )
    
    pins = await ctx.channel.pins()
    
    for i in reversed(pins):

      created = i.created_at
      
      embed.add_field(
        name = str(created.strftime("%m/%d/%Y, %H:%M:%S")),
        value = i.content,
        inline = False
      )

    print("Log sent")
    await ctx.message.delete()
    await ctx.send(embed=embed)

  @commands.command(hidden=True)
  async def tierlist(self,ctx):
    minions = ["Fridge", "x0Fridge", "doucheFridge", "BoobaFridge", "Fridgium", "FridgeOnABridge", "FridgeOnABridgeNearARidgeAndAlso", "FridgeChamp"]

    embed = discord.Embed(
      title = "Fridge Tier List"
    )
    for minion in minions:

      emoji = str(discord.utils.get(self.bot.emojis, name=minion))
      embed.add_field(
        name = str(minions.index(minion) + 1),
        value = emoji,
        inline = False
      )

    await ctx.message.delete()
    await ctx.send(embed=embed)
      

  # GP Giveaway command
  @commands.command(hidden = True,aliases = ["giveaway", "drop"], help = "Starts a giveaway in the current channel. Giveaways will currently last for 5 minutes by default. You must specify the amount of gold to be included in the giveaway. The prize value must be between 100 and 100000\nExample: '.startgiveaway 5000'")
  async def startgiveaway(self, ctx, arg):

    ceo_role = discord.utils.find(lambda r: r.name == 'CEO', ctx.message.guild.roles)

    dev_role = discord.utils.find(lambda r: r.name == 'Bot Dev', ctx.message.guild.roles)

    await ctx.message.delete()
    
    allowed = False
    
    if(ceo_role in ctx.author.roles):
      allowed = True

    if(dev_role in ctx.author.roles):
      allowed = True

    if(allowed == False):
      await ctx.send("You do not have the required role(s) to use this command. Fuck off.")
      return
      
    coins = str(discord.utils.get(self.bot.emojis, name='coins'))
    try:
      prize = int(arg)
    
      if(prize < 100 or prize > 100000):
        raise
    
      time = 300

      dropembed = discord.Embed(
        title = ":partying_face: Drop Party!",
        description = "A drop party has started in <#972947765690765372>"
      )

      dropembed.set_author(name="Log Dog Bot", icon_url=ctx.bot.user.avatar_url)

      await ctx.send(embed=dropembed)
      
      embed = discord.Embed(
        title = ":partying_face: Drop Party! " + coins,
        description = "React with :tada: to enter the giveaway!"
      )

      embed.add_field(
        name = "Prize: ",
        value = str(prize) + " " + coins
      )

      embed.add_field(
        name = "Time Remaining: ",
        value = "5 minute(s)"
      )

      embed.set_author(name="Log Dog Bot", icon_url=ctx.bot.user.avatar_url)

      embed.set_image(url="https://i.imgur.com/Zc4AWrF.png?1")

      giveaway_channel = ctx.bot.get_channel(972947765690765372)
    
      msg = await giveaway_channel.send(embed = embed)
    
      await msg.add_reaction("🎉")

      while time >= 0:
        if time <= 60:
          embed.remove_field(index=1)
          embed.insert_field_at(index=1, name = "Time Remaining: ", value = f"{time} second(s)")
          await msg.edit(embed=embed)
          time -= 2
          await asyncio.sleep(2)
        else:
          embed.remove_field(index=1)
          embed.insert_field_at(index=1, name = "Time Remaining: ", value = f"{int(time/60)} minute(s)")
          await msg.edit(embed=embed)
          time -= 6
          await asyncio.sleep(6)

      if time <= 0:
        embed.remove_field(index = 1)
        embed.insert_field_at(index = 1, name = "Time Remaining: ", value = "Giveaway Ended")
        await msg.edit(embed=embed)

      await asyncio.sleep(time)

      newmsg = await giveaway_channel.fetch_message(msg.id)
    
      users = await newmsg.reactions[0].users().flatten()
    
      users.pop(users.index(self.bot.user))

      if(len(users) == 0):
        winembed = discord.Embed(
          title = "🎉 Drop Party Ended! 🎉",
          description = "Well that's awkward... nobody entered the giveaway"
        )
        await ctx.send(embed=winembed)
        await giveaway_channel.send(embed=winembed)
        return
      
      winner = random.choice(users)
    
      winnerid = str(winner.id)
    
      person = ctx.bot.get_user(int(winner.id))

      await msg.delete()
      
      winembed = discord.Embed(
        title = "🎉 Drop Party Ended! 🎉",
        description = "The winner is... :drum:"
      )

      winembed.add_field(
        name = str(person),
        value="Prize: " + str(prize) + " " + coins
      )

      winembed.set_author(name="Log Dog Bot", icon_url=ctx.bot.user.avatar_url)
    
      winembed.set_footer(text="This money has been sent directly to your bank :)")

      await ctx.send(embed=winembed)

      await giveaway_channel.send(person.mention)
      await giveaway_channel.send(embed=winembed)
    
      if(winnerid in db):
        db[winnerid]["bank"] += prize

      else:
        db[winnerid] = {
          "bal":0,
          "bank":prize
        }
    except Exception as e:
      print(e)
      embed = discord.Embed(title=":x: Drop Party Error :x:",
                           description="Use '.help give' for proper usage of this command")

      await ctx.send(embed=embed)

  # RESETCD COMMAND
  @commands.command(hidden=True)
  async def resetcd(self, ctx, member: discord.Member = None):
    
    user = str(ctx.author.id)
    
    if user != "332601516626280450": return
      
    print("working")

    if(member):

      ctx.author = member
      ctx.message.author = member

      for command in ctx.bot.commands:
        print("command found")
        if command.is_on_cooldown(ctx):
          print("reset succeeded")
          command.reset_cooldown(ctx)
      return
      
    else:
      for command in ctx.bot.commands:
        print("command found")
        if command.is_on_cooldown(ctx):
          print("reset succeeded")
          command.reset_cooldown(ctx)

  @commands.command(hidden=True)
  async def resetallcd(self,ctx):
    
    if str(ctx.author.id) != "332601516626280450": return
      
    guild = ctx.bot.get_guild(893266661698838538)
    
    for member in guild.members:
 
      ctx.author = member
      ctx.message.author = member

      for command in ctx.bot.commands:
        if command.is_on_cooldown(ctx):
          print("reset succeeded for " + member.name)
          command.reset_cooldown(ctx)

    embed = discord.Embed(
      title = "Cooldown Reset",
      description = "Cooldowns for ALL users have been reset!"
    )

    await ctx.send(embed=embed)

  @commands.command(hidden=True)
  async def delinv(self,ctx):
    
    if str(ctx.author.id) != "332601516626280450": return

    user = str(ctx.author.id)

    del db[user]["inv"]

  @commands.command(hidden=True)
  async def giveruby(self,ctx):
    
    if str(ctx.author.id) != "332601516626280450": return

    user = str(ctx.author.id)

    if("ruby" in db[user]["inv"]):

      db[user]["inv"]["ruby"] += 1

    else:

      db[user]["inv"]["ruby"] = 1

def setup(bot):
  bot.add_cog(Admin(bot))