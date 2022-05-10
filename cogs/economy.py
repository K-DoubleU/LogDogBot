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

    # BALANCE COMMAND
    @commands.command(
        aliases=["bal"],
        help="Displays the user's balance, or the balance of a mentioned user")
    async def balance(self, ctx, member: discord.Member = None):

        
        coin_emoji = str(discord.utils.get(self.bot.emojis, name='coins'))
      
        sapphire = str(discord.utils.get(self.bot.emojis, name='sapphire'))
      
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

                embed = discord.Embed(title=":bank: Log Dog Banking")

                embed.add_field(name="Balance",
                                value=str(db[user]["bal"]) + " " + coin_emoji)

                embed.add_field(name="Bank",
                                value=str(db[user]["bank"]) + " " + coin_emoji,
                                inline=False)
              
                # Check for sapphires
                if("inv" in db[user]):
                  if("sapphire" in db[user]["inv"]):

                    sendmsg = str(db[user]["bank"] + db[user]["bal"]) + " " + coin_emoji + "\n" + str(db[user]["inv"]["sapphire"]) + " " + sapphire + "\n**Total:** " + str(db[user]["bank"] + db[user]["bal"] + (db[user]["inv"]["sapphire"] * 420))
                  
                else:
                  sendmsg = str(db[user]["bank"] + db[user]["bal"]) + " " + coin_emoji
                  
                embed.add_field(name="Networth",
                                value=sendmsg,
                                inline=False)

                embed.set_author(name=member.display_name,
                                 icon_url=member.avatar_url)

        else:
          
            user = str(ctx.author.id)

            embed = discord.Embed(title=":bank: Log Dog Banking")

            embed.add_field(name="Balance",
                            value=str(db[user]["bal"]) + " " + coin_emoji)

            embed.add_field(name="Bank",
                            value=str(db[user]["bank"]) + " " + coin_emoji,
                            inline=False)

            # Check for sapphires
            if("inv" in db[user]):
              if("sapphire" in db[user]["inv"]):

                sendmsg = str(db[user]["bank"] + db[user]["bal"]) + " " + coin_emoji + "\n" + str(db[user]["inv"]["sapphire"]) + " " + sapphire + "\n**Total:** " + str(db[user]["bank"] + db[user]["bal"] + (db[user]["inv"]["sapphire"] * 420))
              
              else:
                sendmsg = str(db[user]["bank"] + db[user]["bal"]) + " " + coin_emoji
            else:
              sendmsg = str(db[user]["bank"] + db[user]["bal"]) + " " + coin_emoji
              
            embed.add_field(name="Networth",
                            value=sendmsg,
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

        pick = random.randint(1, 10)
        give = random.randint(20, 75)
        coin_emoji = str(discord.utils.get(self.bot.emojis, name='coins'))

        user = str(ctx.author.id)

        allowed_channels = [972259001062526976,
                         971845967483658260]
        if ctx.channel.id not in allowed_channels:
          await ctx.send("Wrong channel, dumbass")
          ctx.command.reset_cooldown(ctx)
          return

        if(user not in db):
          db[user] = {
            "bal":0,
            "bank":0
          }
          embed = discord.Embed(title="Account created. Please try again")
        # If begging is successful ...
        if pick != 1:

            beg_msg = f"A random stranger gives you some money\nGained: **+{give}**"
            
            embed = discord.Embed(
              title = ":white_check_mark: Begging Successful",
              description = beg_msg + " " + coin_emoji)

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
                value = "You lost: **" + str(give) + "** " + coin_emoji
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
                embed = discord.Embed(
                    title=f":timer: Beg is on cooldown!",
                    description=f"Try again in {minutes} minutes.")

            else:
                embed = discord.Embed(
                    title=f":timer: Beg is on cooldown!",
                    description=f"Try again in {int(error.retry_after)} seconds"
                )

            embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


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
          title = ":coin: Coinflip"
        )

        try:
          if user not in db:
              db[user]["bal"] = 0

          if (arg == "all"):
              amount = db[user]["bal"]
          else:
            amount = int(arg)
            if(amount == 269 or amount == 1045 or amount == 4269): flip = 0

          if (amount > db[user]["bal"]):

              embed.add_field(
                name = ":x: Coinflip Cancelled",
                value ="You don't have this much " + coin_emoji + " dipshit :poop:")

          elif (amount <= 0):

              embed.add_field(
                name = ":x: Coinflip Cancelled",
                value ="Can't flip the air, poor loser :poop:")

          else:

              if (flip == 0):
                  db[user]["bal"] += amount

                  embed.add_field(
                      name = ":partying_face: You WON the coinflip!",
                      value = f"You earned: **+{amount}** " + coin_emoji)
              else:
                  db[user]["bal"] -= amount

                  embed.add_field(
                      name = ":sob: You LOST the coinflip...",
                      value = f"You lost: **-{amount}** " + coin_emoji)

          embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)
        
          await ctx.send(embed=embed)
        
        except Exception as e:
          embed.add_field(
              name = ":x: Coinflip Error :x:",
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
          
        chance = random.randint(1,8)
          
        if member:

          user = str(member.id)
          robbed = str(member.name)

          if(db[user]["bal"] == 0):
              embed = discord.Embed(
                title=":x: Robbery Error :x:",
                description=f"{robbed} has no {coin_emoji} for you to steal!")
              embed.set_author(
                name = ctx.author.display_name,
                icon_url=ctx.author.avatar_url)
              await ctx.send(embed=embed)
              ctx.command.reset_cooldown(ctx)
              return
            
          if user not in db:
            await ctx.send("That user does not have an existing balance")
            ctx.command.reset_cooldown(ctx)
            return
            
          if chance > 2:
            
            winner = str(ctx.author.id)

            max = int(db[user]["bal"] / 3)
            min = int(db[user]["bal"] / 5)

            steal = random.randint(min, max)

            db[user]["bal"] -= steal
            db[winner]["bal"] += steal

            embed = discord.Embed(
              title = ":white_check_mark: Robbery Successful",
              description = f"You robbed {robbed}\nYou stole: **" + str(steal) + "** " + coin_emoji)
            
            embed.set_author(
              name = ctx.author.display_name,
              icon_url=ctx.author.avatar_url)

          else:
            
            caught = False
            
            if(chance == 1):
              caught = True

            if(caught == True):
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
                title = ":x: Robbery Failed",
                description = "You were caught trying to rob " + str(member.name) + ", and were fined " + str(fine) + " " + coin_emoji
                )
              embed.set_author(
                name = ctx.author.display_name,
                icon_url=ctx.author.avatar_url)
            else:
              embed = discord.Embed(
                title = ":x: Robbery Failed",
                description = "You failed your attempt to rob " + str(member.name) + ", but did not get caught!"
                )
              embed.set_author(
                name = ctx.author.display_name,
                icon_url=ctx.author.avatar_url)
              
            
                
        else:
          embed = discord.Embed(
            title=":x: Rob Error :x:",
            description="You must @Mention a user to rob!\nSee 'd.help rob' for more info"
          )
          embed.set_author(
            name = ctx.author.display_name,
            icon_url=ctx.author.avatar_url)

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
                    title=f":timer: Rob is on cooldown!",
                    description=f"Try again in {int(minutes)} minutes")
              
            else:
              
                embed = discord.Embed(
                    title=f":timer: Rob is on cooldown!",
                    description=f"Try again in {int(error.retry_after)} seconds"
                )
            embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)
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
            await ctx.message.delete()
            db[user]["bal"] = int(arg)

    @commands.command(hidden=True)
    async def setbank(self, ctx, member: discord.Member, arg):

        allowed_channels = [972259001062526976,
                         971845967483658260]
        if ctx.channel.id not in allowed_channels:
          await ctx.send("Wrong channel, dumbass")
          return
          
        user = str(member.id)

        if (ctx.author.id != 332601516626280450):
            return
        else:
            await ctx.message.delete()
            db[user]["bank"] = int(arg)


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

        embed = discord.Embed(title=":bank: Log Dog Banking")

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
                embed.add_field(name=":x: Unable to Deposit",
                                value="You don't have " + str(amount) +
                                coin_emoji + " to deposit!")
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return

            if (amount < 0):
                embed.add_field(
                    name=":x: Unable to Deposit",
                    value="You cannot deposit a negative amount of " +
                    coin_emoji)
                await ctx.send(embed=embed)
                ctx.command.reset_cooldown(ctx)
                return
              
            if (amount == 0):
                embed.add_field(
                    name=":x: Unable to Deposit",
                    value=f"You have **0** {coin_emoji} to deposit!")
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
                name=":white_check_mark: Deposit Successful",
                value="Deposited: **" + str(amount) + "** " + coin_emoji +
                "\n\nBank: **" + str(db[user]["bank"]) + "** " + 
                coin_emoji)

            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

        except Exception as e:

            print(e)

            embed.add_field(
                name=":x: Deposit Error :x:",
                value="Use '.help deposit' for proper usage of this command")
          
            ctx.command.reset_cooldown(ctx)

            await ctx.send(embed=embed)

    @deposit.error
    async def deposit_cooldown(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
 
            embed = discord.Embed(
              title=f":timer: Deposit is on cooldown!",
              description=f"Try again in {int(error.retry_after)} seconds"
              )

            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url)

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
        embed = discord.Embed(title=":bank: Log Dog Banking")
        embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url)

        try:

            if(arg == "all"):
              amount = db[user]["bank"]
              if(amount == 0):
                embed.add_field(
                  name = ":x: Withdraw Error",
                  value = "You don't have any " + coin_emoji + " to withdraw!"
                )
                await ctx.send(embed=embed)
                return
              else:
                db[user]["bal"] += db[user]["bank"]
                db[user]["bank"] = 0

                embed.add_field(name=":white_check_mark: Withdraw Success",
                                value="Withdrawn: **" + str(amount) + "** " +
                                coin_emoji)

                await ctx.send(embed=embed)
                return
          
            # If they try to withdraw more than is in their bank, don't allow it
            if int(arg) not in range(1, int(db[user]["bank"]) + 1):

                embed.add_field(name=":x: Withdraw Error",
                                value="Unable to withdraw " + str(arg) + " " +
                                coin_emoji)
                embed.add_field(name="**Bank:**",
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

                embed.add_field(name=":white_check_mark: Withdraw Success",
                                value="Withdrawn: **" + str(arg) + "** " + 
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

        itemlist = {
          "sapphire":420
        }

        emoji = {
          "sapphire" : str(discord.utils.get(self.bot.emojis, name='sapphire'))
        }
      
        final_leaders = {}

        coin_emoji = str(discord.utils.get(self.bot.emojis, name='coins'))
      
        embed = discord.Embed(title="Log Dog Bot Leaderboard")

        embed.set_author(name="Log Dog Bot", icon_url=ctx.bot.user.avatar_url)
        
        for user in db:

            total = 0

            # Only looks for keys that denote balance values
            if ("bal" in db[user]):

                total += db[user]["bal"]

                total += db[user]["bank"]

                # If the user has an inventory, then check if they have items, and add the item values to their networth
                totaltoadd = 0
                if("inv" in db[user]):
                  if(len(db[user]["inv"]) > 0):
                    for item, price in itemlist.items():
                      
                      if(item in db[user]["inv"]):
                        
                        totaltoadd += db[user]["inv"][item] * itemlist[item]
                    
                total += totaltoadd
                final_leaders[user] = total

        for key, value in sorted(final_leaders.items(),
                                 key=lambda item: item[1],
                                 reverse=True)[:10]:

            person = ctx.bot.get_user(int(key))

            printmsg = str(db[key]["bal"] + db[key]["bank"]) + " " + coin_emoji
                                   
            if("inv" in db[key]):
              
              if("sapphire" in db[key]["inv"]):
                
                printmsg = str(db[key]["bal"] + db[key]["bank"]) + " " + coin_emoji + "\n" + str(db[key]["inv"]["sapphire"]) + " " + emoji["sapphire"]
                
            embed.add_field(
              name=person,
              value=printmsg
            )

        embed.set_footer(text="Takes FUCKING FOREVER to load I literally can't fix it I'm sorry, eat my ass")

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
          robbed = str(member.name)
          
          if user not in db:
              await ctx.send("That user does not have an existing bank account")
              ctx.command.reset_cooldown(ctx)
              return

          if(db[user]["bank"] == 0):
              embed = discord.Embed(
                title=":x: Bank Robbery Error :x:",
                description=f"There is no {coin_emoji} in {robbed}'s bank!")
            
              embed.set_author(
                name = ctx.author.display_name,
                icon_url=ctx.author.avatar_url)
            
              await ctx.send(embed=embed)
              ctx.command.reset_cooldown(ctx)
              return
            
          if chance <= 2:
            
            winner = str(ctx.author.id)

            max = int(db[user]["bank"] * .25)
            min = int(db[user]["bank"] * .05)

            steal = random.randint(min, max)

            db[user]["bank"] -= steal
            db[winner]["bal"] += steal

            embed = discord.Embed(title=f"You robbed {robbed}'s bank, and took " + str(steal) + " " + coin_emoji)
            embed.set_author(
                name = ctx.author.display_name,
                icon_url=ctx.author.avatar_url)

          else:

            caught = False
            if(chance >= 7):
              caught = True

            if(caught):
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
                title = ":x: Bank Robbery Failed",
                description = "You were caught trying to rob " + str(member.name) + "'s bank, and were fined " + str(fine) + " " + coin_emoji)
              embed.set_author(
                name = ctx.author.display_name,
                icon_url=ctx.author.avatar_url)

            else:
              embed = discord.Embed(
                title = ":x: Bank Robbery Failed",
                description = "You tried to rob " + str(member.name) + "'s bank, but got nervous and ran away. You were not fined.")
              embed.set_author(
                name = ctx.author.display_name,
                icon_url=ctx.author.avatar_url)
            
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

    @bankrob.error
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
            embed.set_author(
                name = ctx.author.display_name,
                icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)


# PRINTER COMMAND
    @commands.command(aliases=["print"], help="Shows the status of your printer, if you have one")
    async def printer(self,ctx):

      allowed_channels = [972259001062526976,
                         971845967483658260]
      if ctx.channel.id not in allowed_channels:
        await ctx.send("Wrong channel, dumbass")
        return
        
      coins = str(discord.utils.get(self.bot.emojis, name='coins'))
      user = str(ctx.author.id)
      
      embed = discord.Embed(
        title = "Printer Status"
      )

      embed.set_author(
        name = ctx.author.display_name,
        icon_url=ctx.author.avatar_url)

      try:
        if(db[user]["print"] < 100):

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

      allowed_channels = [972259001062526976,
                         971845967483658260]
      if ctx.channel.id not in allowed_channels:
        await ctx.send("Wrong channel, dumbass")
        return
          
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
              "bal":0,
              "bank":0
            }

          if (given > (db[user]["bal"] + db[user]["bank"])):
            embed.add_field(name="You don't have " + str(arg) + " " +
                                coins + " to give!",
                                value=":sob:")

          else:

            remainder = 0
            #Find remainder IF amount is more than the user's balance
            if(given > db[user]["bal"]):
              
              remainder = given - db[user]["bal"]
              
              given = db[user]["bal"]
            
            db[user]["bal"] -= given
            db[user]["bank"] -= remainder

            # Add the amount to the receiver
            db[receiver]["bal"] += (given+remainder)

            embed.add_field(name=f"You gifted {member.name} " + str(arg) + " " +
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

"""
        # Note: No money is given if the sent message is a command
        if message.content.startswith("."):
          return

        # If balance exists, add 1
        elif user in db:

            ratelimit = self.get_ratelimit(message)

            if ratelimit is None:
                db[user]["bal"] += 1

"""

