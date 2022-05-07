import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing
import asyncio

class Misc(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(hidden=True)
  async def geticon(self, ctx):
    icon_url = ctx.guild.icon_url
    await ctx.send(f"The icon url is: {icon_url}")


  # GP Giveaway command
  @commands.command(hidden=True, aliases = ["giveaway", "drop"])
  async def startgiveaway(self, ctx, arg):

    if ctx.author.id != 332601516626280450: return
      
    coins = str(discord.utils.get(self.bot.emojis, name='coins'))
    
    prize = int(arg)

    time = 300

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
    

    await ctx.message.delete()
    
    msg = await ctx.send(embed = embed)
    
    reactions = await msg.add_reaction("🎉")

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

    newmsg = await ctx.fetch_message(msg.id)
    
    users = await newmsg.reactions[0].users().flatten()
    
    users.pop(users.index(self.bot.user))

    winner = random.choice(users)
    
    winnerid = str(winner.id)
    
    person = ctx.bot.get_user(int(winner.id))

    winembed = discord.Embed(
      title = "🎉 Drop Party Ended! 🎉",
      description = "The winner is... :drum:"
    )

    winembed.add_field(
      name = str(person),
      value="Prize: " + str(prize) + " " + coins
    )

    winembed.set_author(name="Log Dog Bot", icon_url=ctx.bot.user.avatar_url)
    
    embed.set_footer(text="This money has been sent directly to your bank :)")

    await ctx.send(embed=winembed)
    
    if(winnerid in db):
      db[winnerid]["bank"] += prize

    else:
      db[winnerid] = {
        "bal":0,
        "bank":prize
      }
    
    

def setup(bot):
  bot.add_cog(Misc(bot))