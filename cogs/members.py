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
  
  @commands.command()
  async def listmembers(self, ctx):

    # First, we will make sure only CEO and Board users can use this command

    ceo_role = discord.utils.find(lambda r: r.name == 'CEO', ctx.message.guild.roles)
    board_role = discord.utils.find(lambda r: r.name == 'Board', ctx.message.guild.roles)

    allowed = False
    
    if(ceo_role in ctx.author.roles):
      allowed = True

    if(board_role in ctx.author.roles):
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
          
          for role in roles:
            
              if(role in member.roles):
                
                excluded = True

          if(excluded == False and member.bot == False):
            
            print(member)   
            list += str(member) + "\n"  

    embed = discord.Embed(
          title = "Log Dog Member List",
          description = list
        )
    
    await ctx.send(embed=embed)


def setup(bot):
  bot.add_cog(Members(bot))