import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing

class Members(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(hidden=True)
  async def listmembers(self, ctx):

    # First, we will make sure only CEO and Board users can use this command

    ceo_role = discord.utils.find(lambda r: r.name == 'CEO', ctx.message.guild.roles)
    board_role = discord.utils.find(lambda r: r.name == 'Board', ctx.message.guild.roles)
    dev_role = discord.utils.find(lambda r: r.name == 'Bot Dev', ctx.message.guild.roles)

    allowed = False
    
    if(ceo_role in ctx.author.roles):
      allowed = True

    if(board_role in ctx.author.roles):
      allowed = True

    if(dev_role in ctx.author.roles):
      allowed = True

    if(allowed == False):
      await ctx.send("You do not have the required role(s) to use this command. Fuck off.")
      return

    # If the user passes the test above, and has the required role(s), the rest of the function is executed
      
    list = ""
    roles = [discord.utils.find(lambda r: r.name == 'CEO', ctx.message.guild.roles),
            discord.utils.find(lambda r: r.name == 'Board', ctx.message.guild.roles),
            discord.utils.find(lambda r: r.name == 'Clan Friend', ctx.message.guild.roles),
            discord.utils.find(lambda r: r.name == 'Staff', ctx.message.guild.roles)]
    
    for guild in ctx.bot.guilds:
      
        for member in guild.members:

          excluded = False

          if(str(member.id) in db): 
            active = True
          else: 
            active = False
          
          for role in roles:
            
              if(role in member.roles):
                
                excluded = True

          if(excluded == False and member.bot == False):
            
            print(member)   
            list += str(member) + " - Active: " + str(active) + "\n"  

    list1 = list[0:4019]
    list2 = list[4019:]
    
    embed = discord.Embed(
          title = "Log Dog Member List - Page 1",
          description = list1
        )
    embed2 = discord.Embed(
          title = "Log Dog Member List - Page 2",
          description = list2
        )

    
    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)
    
  @commands.command(hidden=True)
  async def listdb(self, ctx):

    if ctx.author.id != 332601516626280450: return
      
    embed = discord.Embed(title="All key-value entries in db - Page 1")
    embed2 = discord.Embed(title="All key-value entries in db - Page 2")

    i = 0
    for key, value in db.items():
      
      field_value = ""

      
      for a, b in value.items():

        
        field_value += f"{a} = {b}\n"
        
        
      person = ctx.bot.get_user(int(key))

      if(i > 24):
        embed2.add_field(
          name = person,
          value = field_value
        )
      else:
        embed.add_field(
          name = person,
          value = field_value
        )
      i += 1
      
    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)

def setup(bot):
  bot.add_cog(Members(bot))