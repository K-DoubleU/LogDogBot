import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing

class Economy(commands.Cog):
  
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(
            1, 60, commands.BucketType.member)

    def get_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        """Returns the ratelimit left"""
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")

    # MESSAGE LISTENER TO GIVE MONEY
    # Gives the user 1 point whenever they send a message
    @commands.Cog.listener()
    async def on_message(self, message):

      
        if message.author == self.bot.user:
            return

        user = str(message.author.id)

        # Tests if the message was sent by a bot. If it was, then delete the user from the db and exit the command
        if message.author.bot == True:
            return

        if user not in db:
            db[user] = {
              "bal":0,
              "bank":0
            }

        # Note: No money is given if the sent message is a command
        if message.content.startswith("."):
          return

        # If balance exists, add 1
        elif user in db:

            ratelimit = self.get_ratelimit(message)

            if ratelimit is None:
                db[user]["bal"] += 1


    # BALANCE COMMAND
    @commands.command(
        aliases=["bal"],
        help="Displays the user's balance, or the balance of a mentioned user")
    async def balance(self, ctx, member: discord.Member = None):

        coin_emoji = str(discord.utils.get(self.bot.emojis, name='coins'))
        user = str(ctx.author.id)

        allowed_channels = [972259001062526976,
                         971845967483658260]
        if ctx.channel.id not in allowed_channels:
          await ctx.send("Wrong channel, dumbass")
          return
          
        if (member):

            if (member == ctx.bot.user):
                bal_msg = "Log Dog Bot will not let you see their balance!"

                embed = discord.Embed(title=bal_msg + " :rage:")
                embed.set_author(name="Log Dog Bot",
                                 icon_url=ctx.bot.user.avatar_url)

            else:

                user = str(member.id)

                embed = discord.Embed(title=str(member.name) + "#" +
                                      str(member.discriminator))

                embed.add_field(name="Balance",
                                value=str(db[user]["bal"]) + " " + coin_emoji)

                embed.add_field(name="Bank",
                                value=str(db[user]["bank"]) + " " + coin_emoji,
                                inline=False)
              
                embed.add_field(name="Networth",
                                value=str(db[user]["bank"] + db[user]["bal"]) + " " + coin_emoji,
                                inline=False)

                embed.set_author(name=member.display_name,
                                 icon_url=member.avatar_url)

        else:
          
            user = str(ctx.author.id)

            embed = discord.Embed(title=str(ctx.author.name) + "#" +
                                  str(ctx.author.discriminator))

            embed.add_field(name="Balance",
                            value=str(db[user]["bal"]) + " " + coin_emoji)

            embed.add_field(name="Bank",
                            value=str(db[user]["bank"]) + " " + coin_emoji,
                            inline=False)
            embed.add_field(name="Networth",
                                value=str(db[user]["bank"] + db[user]["bal"]) + " " + coin_emoji,
                                inline=False)

            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url)

        if user not in db:
            db[user]["bal"] = 0

        await ctx.send(embed=embed)


    # BEG COMMAND
    @commands.command(
        help=
        "Beg for gp, with a 80% chance to receive some gp. Has a 20% chance to get mugged and lose money instead\nCooldown: 5 Minutes"
    )
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def beg(self, ctx):

        pick = random.randint(1, 8)
        give = random.randint(20, 75)
        coin_emoji = str(discord.utils.get(self.bot.emojis, name='coins'))

        user = str(ctx.author.id)

        allowed_channels = [972259001062526976,
                         971845967483658260]
        if ctx.channel.id not in allowed_channels:
          await ctx.send("Wrong channel, dumbass")
          ctx.command.reset_cooldown(ctx)
          return

        # If begging is successful ...
        if pick != 1:

            beg_msg = f"After begging random strangers, somebody gives you {give} "
            
            embed = discord.Embed(title=beg_msg + " " + coin_emoji, )

            if user in db:
                db[user]["bal"] += give
            else:
                db[user]["bal"] = give

        # If begging fails ... 
        else:

            # If they have less than what was taken from them, change the amount taken to the exact amount they have in their balance
            if (db[user]["bal"] <= give):
                give = db[user]["bal"]

            embed = discord.Embed(
              title = "You Got Mugged!",
              description = "Somebody gets annoyed with your begging... and mugs you!"
            )

            if(give != 0):
              embed.add_field(
                name = "You lost: ",
                value = str(give) + " " + coin_emoji
              )
            else:
              embed.add_field(
                name = "Oh... you didn't have any money on you.",
                value = "You lost " + str(give) + " " + coin_emoji
              )

            if (user not in db):
                db[user]["bal"] = 0
            else:
                db[user]["bal"] -= give

              

        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @beg.error
    async def beg_cooldown(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            minutes = round(error.retry_after / 60)

            if (error.retry_after >= 60):
                em = discord.Embed(
                    title=f"Beg is on cooldown!",
                    description=f"Try again in {minutes} minutes.")

            else:
                em = discord.Embed(
                    title=f"Beg is on cooldown!",
                    description=f"Try again in {int(error.retry_after)} seconds"
                )

            em.set_author(name="Log Dog Bot", icon_url=ctx.bot.user.avatar_url)

        await ctx.send(embed=em)


    # COINFLIP COMMAND
    @commands.command(
        help=
        "Bets however much gp you specify, with a 50/50 chance to either double or lose your money",
      aliases = ["cf", "gamble", "flip"]
    )
    async def coinflip(self, ctx, arg=None):

        allowed_channels = [972259001062526976,
                         971845967483658260]
        if ctx.channel.id not in allowed_channels:
          await ctx.send("Wrong channel, dumbass")
          return
          
        flip = random.randint(0, 1)
        user = str(ctx.author.id)
        coin_emoji = str(discord.utils.get(self.bot.emojis, name='coins'))

        embed = discord.Embed(
          title = "Coinflip"
        )

        try:
          if user not in db:
              db[user]["bal"] = 0

          if (arg == "all"):
              amount = db[user]["bal"]
          else:
              amount = int(arg)

          if (amount > db[user]["bal"]):

              embed.add_field(
                name = "Coinflip Error",
                value ="You don't have this much " + coin_emoji + " dipshit :poop:")

          elif (amount <= 0):

              embed.add_field(
                name = "Coinflip Error",
                value ="Can't flip the air, poor loser :poop:")

          else:

              if (flip == 0):
                  db[user]["bal"] += amount

                  embed.add_field(
                      name = "You won the coinflip!",
                      value = f"You earned {amount} " + coin_emoji)
              else:
                  db[user]["bal"] -= amount

                  embed.add_field(
                      name = "You lost the coinflip...",
                      value = f"You lost {amount} " + coin_emoji)

          embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)
        
          await ctx.send(embed=embed)
        
        except Exception as e:
          embed.add_field(
              name = "Coinflip Error",
              value = "Use '.help coinflip' for proper usage of this command")
          await ctx.send(embed=embed)
          
      
    # ROB COMMAND
    @commands.command(
        aliases=["steal"],
        help="Steals gp from a mentioned user\nCooldown: 15 Minutes")
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member = None):

      allowed_channels = [972259001062526976,
                         971845967483658260]
      if ctx.channel.id not in allowed_channels:
          await ctx.send("Wrong channel, dumbass")
          ctx.command.reset_cooldown(ctx)
          return
        
      coin_emoji = str(discord.utils.get(self.bot.emojis, name='coins'))
      
      try:

        if("@" not in ctx.message.content): 

          ctx.command.reset_cooldown(ctx)
          raise 
          
        chance = random.randint(1,5)
          
        if member:

          user = str(member.id)

          if user not in db:
            await ctx.send("That user does not have an existing balance")
            ctx.command.reset_cooldown(ctx)
            return
            
          if chance != 1:
            
            winner = str(ctx.author.id)

            robbed = str(member.name)

            max = int(db[user]["bal"] / 3)

            steal = random.randint(0, max)

            db[user]["bal"] -= steal
            db[winner]["bal"] += steal

            embed = discord.Embed(title=f"You robbed {robbed}, and took " + str(steal) + " " + coin_emoji)

          else:

              # Generates the amount fined if caught
            fine = random.randint(25, 150)

              # Here we grab the author's balance and bank entries
            user = str(ctx.author.id)

            # If the amount generated is higher than their networth, change the fine to their networth
            networth = db[user]["bal"] + db[user]["bank"]
            if(fine > networth):
              fine = networth
              # If their fine is the same as their balance OR less, than we just subtract it from their balance, no need to go into bank
            if(fine <= db[user]["bal"]):
              db[user]["bal"] -= fine
            else:
              # If fine is higher than what they have on hand, we set a variable to the remainder after subtracting what the user has on hand
              remainder = fine - int(db[user]["bal"])
              

              db[user]["bal"] = 0

              # Also need to account for bank not having enough, so that we don't push them into the negative
              if(remainder > db[user]["bank"]):
                db[user]["bank"] = 0
              # If they have enough in their bank, just subtract the remainder from the bank
              else:
                db[user]["bank"] -= remainder
                
              # Build embed for failure
            embed = discord.Embed(
              title = "Robbery Failed",
              description = "You were caught trying to rob " + str(member.name) + ", and were fined " + str(fine) + coin_emoji
              )
                
        else:
          embed = discord.Embed(
            title="Rob Error",
            description="You must @Mention a user to rob!\nSee 'd.help rob' for more info"
          )

          await ctx.send(embed=embed)
          ctx.command.reset_cooldown(ctx)
          return

        await ctx.send(embed=embed)
        
      except Exception as e:

            print(e)

            embed = discord.Embed(
                title=":x: Rob Error :x:",
                description="Use '.help rob' for proper usage of this command")

            await ctx.send(embed=embed)

    @rob.error
    async def rob_cooldown(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            minutes = round(error.retry_after / 60)

            if (error.retry_after > 60):
              
                embed = discord.Embed(
                    title=f"Rob is on cooldown!",
                    description=f"Try again in {int(minutes)} minutes")
              
            else:
              
                embed = discord.Embed(
                    title=f"Rob is on cooldown!",
                    description=f"Try again in {int(error.retry_after)} seconds"
                )
            embed.set_author(name="Log Dog Bot", icon_url=ctx.bot.user.avatar_url)
            await ctx.send(embed=embed)


    # SET COMMAND
    @commands.command(hidden=True)
    async def set(self, ctx, member: discord.Member, arg):

        allowed_channels = [972259001062526976,
                         971845967483658260]
        if ctx.channel.id not in allowed_channels:
          await ctx.send("Wrong channel, dumbass")
          return
          
        user = str(member.id)

        if (ctx.author.id != 332601516626280450):
            return
        else:
            db[user]["bal"] = int(arg)


    # DEPOSIT COMMAND
    @commands.command(
        aliases=["bank", "dep"],
        help=
        "Deposit gp into your bank. Coins in your bank cannot be stolen from other users, or lost from failed beg attempts.\nYou can use '.deposit all' to deposit your entire balance"
    )
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def deposit(self, ctx, arg=None):

        allowed_channels = [972259001062526976,
                         971845967483658260]
        if ctx.channel.id not in allowed_channels:
          await ctx.send("Wrong channel, dumbass")
          ctx.command.reset_cooldown(ctx)
          return
      
        coin_emoji = str(discord.utils.get(self.bot.emojis, name='coins'))

        user = str(ctx.author.id)

        embed = discord.Embed(title="Log Dog Banking")

        # First, checks to see if the user provided an argument
        # If not, we default to it being 0

        try:

            # If the arg provided is the word "all" we change the amount to whatever the total balance of the user is
            if (arg == "all"):
                amount = int(db[user]["bal"])
            else:
                # If it's an integer, we assign it to the variable amount
                amount = int(arg)

            # Here we handle different cases, including any errors
            # If the user enters more money than is in their balance, return an error and exit the command
            if (amount > db[user]["bal"]):
                embed.add_field(name="Unable to Deposit",
                                value="You don't have " + str(amount) +
                                coin_emoji + " to deposit!")
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return

            if (amount < 0):
                embed.add_field(
                    name="Unable to Deposit",
                    value="You cannot deposit a negative amount of " +
                    coin_emoji)
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
              
            if (amount == 0):
                embed.add_field(
                    name="Unable to Deposit",
                    value="You have no money to deposit!")
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return

            # Otherwise, if the argument is a valid number, then we make the deposit
            if user not in db:
                db[user]["bank"] = amount
            else:
                db[user]["bank"] += amount

            db[user]["bal"] -= amount

            embed.add_field(
                name="Deposit Successful",
                value="You deposited " + str(amount) + " " + coin_emoji +
                " into your bank!\nCurrent Bank Balance: " + str(db[user]["bank"]) + " " + 
                coin_emoji)

            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

        except Exception as e:

            print(e)

            embed.add_field(
                name="Deposit Error",
                value="Use '.help deposit' for proper usage of this command")
          
            ctx.command.reset_cooldown(ctx)

            await ctx.send(embed=embed)

    @deposit.error
    async def deposit_cooldown(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
 
            embed = discord.Embed(
              title=f"Deposit is on cooldown!",
              description=f"Try again in {int(error.retry_after)} seconds"
              )

            embed.set_author(name="Log Dog Bot", icon_url=ctx.bot.user.avatar_url)

            await ctx.send(embed=embed)

    # WITHDRAW COMMAND
    @commands.command(aliases=["wd"],
                      help="Move money from your bank to your balance.")
    async def withdraw(self, ctx, arg):

        allowed_channels = [972259001062526976,
                         971845967483658260]
        if ctx.channel.id not in allowed_channels:
          await ctx.send("Wrong channel, dumbass")
          return
      
        user = str(ctx.author.id)
        coin_emoji = str(discord.utils.get(self.bot.emojis, name='coins'))

        # Begin embed construction
        embed = discord.Embed(title="Log Dog Banking")

        try:

            if(arg == "all"):
              amount = db[user]["bank"]
              if(amount == 0):
                embed.add_field(
                  name = "Withdraw Error",
                  value = "You don't have any " + coin_emoji + " to withdraw!"
                )
                await ctx.send(embed=embed)
                return
              else:
                db[user]["bal"] += db[user]["bank"]
                db[user]["bank"] = 0

                embed.add_field(name="Withdraw Success",
                                value="You have withdrawn " + str(amount) + " " +
                                coin_emoji)

                await ctx.send(embed=embed)
                return
          
            # If they try to withdraw more than is in their bank, don't allow it
            if int(arg) not in range(1, int(db[user]["bank"]) + 1):

                embed.add_field(name=":x: Withdraw Error :x:",
                                value="Unable to withdraw " + str(arg) + " " +
                                coin_emoji)
                embed.add_field(name="Your bank balance:",
                                value=str(db[user]["bank"]) + " " + coin_emoji,
                               inline = False)

                await ctx.send(embed=embed)
                return

            elif (int(arg) <= 0):

                embed.add_field(name=":x: Withdraw Error :x:",
                                value="You cannot withdraw less than 1 " +
                                coin_emoji)

                await ctx.send(embed=embed)
                return

            else:

                db[user]["bal"] += int(arg)
                db[user]["bank"] -= int(arg)

                embed.add_field(name="Withdraw Success",
                                value="You have withdrawn " + str(arg) + " " + 
                                coin_emoji)

                await ctx.send(embed=embed)

        except Exception as e:
            print(e)
            embed.add_field(
                name=":x: Withdraw Error :x:",
                value="Use '.help withdraw' for proper usage of this command")

            await ctx.send(embed=embed)

# LEADERBOARD COMMAND

    @commands.command(aliases=["leader", "board", "leaders", "lb"])
    async def leaderboard(self, ctx):

        allowed_channels = [972259001062526976,
                         971845967483658260]
        if ctx.channel.id not in allowed_channels:
            await ctx.send("Wrong channel, dumbass")
            return
          
        final_leaders = {}

        coin_emoji = str(discord.utils.get(self.bot.emojis, name='coins'))
      
        embed = discord.Embed(title="GP Leaderboard")
        
        for user in db:

            total = 0

            # Only looks for keys that denote balance values
            if ("bal" in db[user]):

                total += db[user]["bal"]

                total += db[user]["bank"]

                final_leaders[user] = total

        for key, value in sorted(final_leaders.items(),
                                 key=lambda item: item[1],
                                 reverse=True)[:10]:

            person = ctx.bot.get_user(int(key))

            embed.add_field(name=person, value=str(value) + " " + coin_emoji)

        await ctx.send(embed=embed)

# BANKROB COMMAND
    @commands.command(
        aliases=["robbank"],
        help="Steals gp from a mentioned user's bank.\nSuccess rate: 20%\nCooldown: 3 Hours")
    @commands.cooldown(1, 10800, commands.BucketType.user)
    async def bankrob(self, ctx, member: discord.Member = None):

      allowed_channels = [972259001062526976,
                         971845967483658260]
      if ctx.channel.id not in allowed_channels:
          await ctx.send("Wrong channel, dumbass")
          ctx.command.reset_cooldown(ctx)
          return
        
      coin_emoji = str(discord.utils.get(self.bot.emojis, name='coins'))
      
      try:
        
        chance = random.randint(1,10)
          
        if member:
          
          user = str(member.id)
          
          if user not in db:
              await ctx.send("That user does not have an existing bank account")
              ctx.command.reset_cooldown(ctx)
              return
            
          if chance <= 2:
            
            winner = str(ctx.author.id)

            robbed = str(member.name)

            max = int(db[user]["bank"] / 3)

            steal = random.randint(0, max)

            db[user]["bank"] -= steal
            db[winner]["bal"] += steal

            embed = discord.Embed(title=f"You robbed {robbed}'s bank, and took " + str(steal) + " " + coin_emoji)

          else:

              # Generates the amount fined if caught
            fine = random.randint(50, 400)

              # Here we grab the author's balance and bank entries
            user = str(ctx.author.id)

            # If the amount generated is higher than their networth, change the fine to their networth
            networth = db[user]["bal"] + db[user]["bank"]
            if(fine > networth):
              fine = networth
              # If their fine is the same as their balance OR less, than we just subtract it from their balance, no need to go into bank
            if(fine <= db[user]["bal"]):
              db[user]["bal"] -= fine
            else:
              # If fine is higher than what they have on hand, we set a variable to the remainder after subtracting what the user has on hand
              remainder = fine - int(db[user]["bal"])
             

              db[user]["bal"] = 0

              # Also need to account for bank not having enough, so that we don't push them into the negative
              if(remainder > db[user]["bank"]):
                db[user]["bank"] = 0
              # If they have enough in their bank, just subtract the remainder from the bank
              else:
                db[user]["bank"] -= remainder
                
            # Build embed for failure
            embed = discord.Embed(
              title = "Robbery Failed",
              description = "You were caught trying to rob " + str(member.name) + "'s bank, and were fined " + str(fine) + " " + coin_emoji)
            
        else:
          embed = discord.Embed(
            title=":x: Bankrob Error :x:",
            description="You must @Mention a user to rob!\nSee '.help bankrob' for more info"
          )

          await ctx.send(embed=embed)
          ctx.command.reset_cooldown(ctx)
          return

        await ctx.send(embed=embed)
        
      except Exception as e:

            print(e)

            embed = discord.Embed(
                title=":x: Bankrob Error :x:",
                description="Use '.help bankrob' for proper usage of this command")

            await ctx.send(embed=embed)

    @ bankrob.error
    async def bankrob_cooldown(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            minutes = round(error.retry_after / 60)

            if(error.retry_after >= 3600):
                embed = discord.Embed(
                    title=f"Bankrob is on cooldown!",
                    description=f"Try again in {int(minutes/60)} hours")
              
            elif (error.retry_after > 60):
              
                embed = discord.Embed(
                    title=f"Bankrob is on cooldown!",
                    description=f"Try again in {int(minutes)} minutes")
              
            else:
              
                embed = discord.Embed(
                    title=f"Bankrob is on cooldown!",
                    description=f"Try again in {int(error.retry_after)} seconds"
                )
            embed.set_author(name="Log Dog Bot", icon_url=ctx.bot.user.avatar_url)
            await ctx.send(embed=embed)


# PRINTER COMMAND
    @commands.command(aliases=["print"], help="Shows the status of your printer, if you have one")
    async def printer(self,ctx):

      coins = str(discord.utils.get(self.bot.emojis, name='coins'))
      user = str(ctx.author.id)
      
      embed = discord.Embed(
        title = "Printer Status"
      )

      try:
        if(db[user]["print"] < 10):

          embed.add_field(
            name = "No Printer Active",
            value = "Purchase a printer in the Grand Exchange!"
          )
          await ctx.send(embed=embed)
        else:

          embed.add_field(
            name = "Printer Active",
            value = "Your printer is generating " + str(db[user]["print"]) + " " + coins + " per hour"
          )
          await ctx.send(embed=embed)
          
      except Exception as e:

        print(e)
        
        embed = discord.Embed(
        title = "Printer Status"
        )
        embed.add_field(
          name = "No Printer Active",
          value = "Purchase a printer in the Grand Exchange!"
          )
        await ctx.send(embed=embed)
        
    # Testing command to reset printer
    @commands.command(hidden=True)
    async def resetprinter(self, ctx):
      if ctx.author.id != 332601516626280450: return

      user = str(ctx.author.id)
      del db[user]["print"]


 # GIVE COMMAND
    @commands.command(
        aliases=["gift"],
        help=
        "Give someone a specified amount of gp. The money will be taken from the user, and given to the recipient"
    )
    async def give(self, ctx, member: discord.Member=None, arg=0):

      coins = str(discord.utils.get(self.bot.emojis, name='coins'))

      user = str(ctx.author.id)

      try:

        embed = discord.Embed(title="GP Gift")

        if member:
          receiver = str(member.id)
          given = int(arg)

          if(given <= 0):
            embed.add_field(
              name=":x: Gifting Error :x:",
              value="You cannot gift less than 1" + coins)
            
            await ctx.send(embed = embed)
            
            return

          if receiver not in db:
            db[receiver] = {
              "bal":given,
              "bank":0
            }

          if (given > db[user]["bal"]):
            embed.add_field(name="You don't have " + str(arg) + " " +
                                coins + " to give!",
                                value=":sob:")

          else:
            db[user]["bal"] -= given
            db[receiver]["bal"] += given

            embed.add_field(name=f"You gifted {member.name} " + str(arg) +
                                coins,
                                value=":tada:")
        else:
          embed.add_field(
            name=":x: Gifting Error :x:",
            value="Use '.help give' for proper usage of this command")
          await ctx.send(embed = embed)
          return

        await ctx.send(embed=embed)
      except Exception as e:
        print(e)

        embed.add_field(
          name=":x: Gifting Error :x:",
          value="Use '.help give' for proper usage of this command")
        await ctx.send(embed=embed)
      
    @give.error
    async def give_error(self, ctx, error):
      embed = discord.Embed(title="GP Gift")
      
      if isinstance(error, commands.BadArgument):
        embed.add_field(
                name=":x: Gifting Error :x:",
                value="Use '.help give' for proper usage of this command")
        await ctx.send(embed=embed)
          
def setup(bot):
    bot.add_cog(Economy(bot))



