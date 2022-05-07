import discord
import os
import requests
import json
from keep_alive import keep_alive
from discord.ext import commands
from discord.ext import tasks
from replit import db


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=".",intents=intents)

#event for when bot goes online and is running
# WAS MOVED TO ECONOMY.PY FOR NOW

cogs = ["cogs.members", "cogs.lvnd", "cogs.economy", "cogs.shop", "cogs.misc"]


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

@tasks.loop(seconds=3600)
async def hourly_gp():
    for user in db:
      if("print" in db[user]):
        
          # Grabs the printlvl of the user, and only increases their bal based on the printlvl

        if(db[user]["print"] == 10): 
          db[user]["bal"] += 10
          print(user + " increased by " + str(db[user]["print"]))
      
              
@bot.command(hidden=True)
async def ping(ctx):
    await ctx.send(f"Bot latency: {round(bot.latency * 1000)}ms")


@bot.command(pass_content=True, aliases = ["cd", "cooldown"], help="Displays all current cooldowns for the user")
async def cooldowns(ctx):
  cooldown_string = ""

  embed = discord.Embed(
    title = str(ctx.author) + "'s Cooldowns"
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


hourly_gp.start()
#Run the bot and keep it online
keep_alive()

bot.run(os.getenv('TOKEN'))