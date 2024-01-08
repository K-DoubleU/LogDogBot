import discord
import os
import requests
import json
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=".",intents=discord.Intents.all())

cogs = [
    # "cogs.members",
    "cogs.admin",
    "cogs.misc"]


# This event occurs whenever the bot is started up. This will run every time the bot is restarted.
@bot.event
async def on_ready():
    print("The bot is ready!")
    print("Loading cogs . . .")
    # Iterate through the "cogs" list
    for cog in cogs:
        try:
            # Loads each extension specified in the cogs list
            bot.load_extension(cog)
            print(cog + " was loaded.")

# If an error occurs with trying to load a cog, print the error to the console
        except Exception as e:
            print(e)


# @bot.event
# async def on_member_join(member):
#
#     person = str(member.id)
#     logdoggerid = 893277099350163518
#     logdoggerrole = get(member.guild.roles, id = logdoggerid)
#
#     if(person in db):
#       if("clan" in db[person]):
#         await member.add_roles(logdoggerrole)


@bot.command(hidden=True)
async def ping(ctx):
    await ctx.send(f"Bot latency: {round(bot.latency * 1000)}ms")




@bot.command(pass_content=True, aliases = ["cd", "cooldown"], help="Displays all current cooldowns for the user")
async def cooldowns(ctx):
  cooldown_string = ""

  embed = discord.Embed(
    title = ":timer: " + str(ctx.author.name) + "'s Cooldowns"
  )
  
  for command in bot.commands:
    
    if command.is_on_cooldown(ctx):

      time = round(int(command.get_cooldown_retry_after(ctx)))

      if(time > 3600):
        embed.add_field(
          name = f"**{command}**",
          value = f"{round((time/60)/60)} hours"
        )
      elif(time < 60):
        embed.add_field(
          name = f"**{command}**",
          value = f"{time} seconds"
        )
      else:
        embed.add_field(
          name = f"**{command}**",
          value = f"{round(time/60)} minutes"
        )
      cooldown_string += f"\n{command} - **Time Left:** {command.get_cooldown_retry_after(ctx)}MS"

  if cooldown_string == "":
    embed.add_field(
      name = "No Cooldowns",
      value = "Go Crazy!"
    )

  embed.set_author(
    name=ctx.author.display_name,
    icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)


# This is where we override the default help command. Putting this in main.py for now, cannot get this to work from within a separate Cog


class MyHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:

            # Creates our embed for the help message
            embed = discord.Embed(title="Help Menu", description=page)

            # Sets author of embed
            embed.set_author(name="Log Dog Bot", icon_url=bot.user.avatar_url)

            # embed.set_thumbnail(url="")
            embed.set_thumbnail(url="https://i.imgur.com/Igx5Xa6.png")

            embed.set_footer(text="Bot developed and managed by Dissy#5926")
            await destination.send(embed=embed)


# Replaces the default command by constructing an instance of MyHelp, which overrides some aspects of MinimalHelpCommand
bot.help_command = MyHelp()


# If repl ip is getting banned due to rate-limits, type 'kill 1' into Shell to reset ip


#Run the bot and keep it online

bot.run(os.getenv('TOKEN'))