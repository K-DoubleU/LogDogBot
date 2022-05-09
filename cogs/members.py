import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing
from datetime import datetime

"""
1-2 bandos
3-4 zaros
5-6 arma
7-9 zammy
10-12 sara
13-16 guth
17+ seren
"""

# create global ign list
ign_list = {
   "02 my waifu":	"9,Mar,2022",
   "0nuzq":	"29,May,2021",
   "1 A N D 1":	"10,Oct,2021",
   "1 inv andy":	"9,Sep,2021",
   "340":	"17,Feb,2022",
   "8pocket42":	"21,Aug,2021",
   "A_SeaTurtle":	"1,May,2022",
   "Aceinthewhat":	"13,Sep,2021",
   "aGamerGaming":	"4,Sep,2021",
   "Agent Clank":	"30,May,2021",
   "AhaShakes":	"7,Jul,2021",
   "Alexmaee":	"28,May,2021",
   "ali airball":	"5,Oct,2021",
   "Anjru":	"29,Aug,2021",
   "AoA Entei":	"26,Aug,2021",
   "AoA Solgaleo":	"7,Oct,2021",
   "AoA Zacian":	"15,Sep,2021",
   "Apepoc":	"23,Jun,2021",
   "arrg you srs":	"29,Dec,2021",
   "Atypia":	"5,Feb,2022",
   "avrg":	"22,Aug,2021",
   "ayrball":	"7,Feb,2022",
   "Bacoid1":	"13,Jan,2022",
   "bacoidthe4th":	"27,Mar,2022",
   "BAMB0NG":	"31,Jan,2022",
   "Bee Bae":	"3,May,2022",
   "bee safe":	"3,Jun,2021",
   "BlendingTime":	"28,May,2021",
   "boile y":	"22,Feb,2022",
   "boobs420":	"9,Mar,2022",
   "Born Soft":	"3,Feb,2022",
   "Bow And K0":	"9,Jan,2022",
   "bo bby":	"12,Oct,2021",
   "Brando Jamz":	"12,Jan,2022",
   "Bretters":	"1,May,2022",
   "brutwoburst":	"21,Nov,2021",
   "Bubblenab":	"28,May,2021",
   "BUD LlGHTS":	"17,Aug,2021",
   "buying 2x P":	"7,Feb,2022",
   "b oe":	"3,Feb,2022",
   "b rfb":	"29,Oct,2021",
   "Capn Tj":	"20,Aug,2021",
   "Caring":	"1,Jan,2022",
   "Cerastease":	"2,Nov,2021",
   "Chasx":	"20,Aug,2021",
   "ChefBoyArtyy":	"7,Jan,2022",
   "Chronology":	"29,Dec,2021",
   "ClaasJaguar":	"18,Dec,2021",
   "ClassyWizKey":	"21,Oct,2021",
   "Clipper":	"12,Feb,2022",
   "cloud zen":	"16,Nov,2021",
   "Colbby":	"8,Aug,2021",
   "Comrade Fyre":	"7,Oct,2021",
   "Consistent C":	"2,Mar,2022",
   "coolchub":	"26,Jan,2022",
   "coxieBlood":	"26,Jul,2021",
   "coxieDino":	"15,Aug,2021",
   "Cp Teemo":	"28,May,2021",
   "CrimsonGFX":	"8,Jan,2022",
   "cupma":	"26,Aug,2021",
   "C himera":	"3,Jan,2022",
   "c h u c kles":	"21,Aug,2021",
   "C L Y":	"28,May,2021",
   "C olbby":	"10,Jul,2021",
   "Darkrise":	"24,Aug,2021",
   "DatNeck":	"28,May,2021",
   "Deli Barista":	"30,Dec,2021",
   "Deli Cashier":	"31,Dec,2021",
   "Delystbro":	"14,Sep,2021",
   "Delystt":	"23,Aug,2021",
   "dombcat":	"9,Oct,2021",
   "Doodstil":	"20,Nov,2021",
   "Dorvagten":	"26,Apr,2022",
   "Do It Myself":	"27,Nov,2021",
   "Dreww":	"20,Dec,2021",
   "dxamfetamine":	"3,Dec,2021",
   "D o n s o n":	"21,Aug,2021",
   "earf flat":	"10,Dec,2021",
   "EarthNoGlobe":	"24,Nov,2021",
   "ElonGrip":	"4,Oct,2021",
   "Elwood":	"18,Feb,2022",
   "enzo_O":	"28,Jan,2022",
   "EpicGamer69":	"1,Apr,2022",
   "eVirgin":	"30,Jan,2022",
   "Ez 4 Easy":	"27,Dec,2021",
   "FAILED ZEUS":	"22,Aug,2021",
   "farmers4life":	"5,Oct,2021",
   "FDM":	"23,Oct,2021",
   "fe iris":	"8,Jan,2022",
   "Fe Maui":	"1,Dec,2021",
   "Fioriture":	"26,Jan,2022",
   "fkn help":	"27,Jul,2021",
   "free iris":	"9,Apr,2022",
   "Gerglidor":	"19,Dec,2021",
   "Gewni":	"13,Aug,2021",
   "Gewnster":	"12,Jul,2021",
   "GIM902RANGER":	"7,Jan,2022",
   "GIMitalia":	"15,Nov,2021",
   "GIM Zeus FTB":	"7,Oct,2021",
   "glancer4life":	"5,Oct,2021",
   "GlizzyL":	"31,Dec,2021",
   "Globe Denier":	"2,Nov,2021",
   "Gmar":	"1,Sep,2021",
   "Gnarly Nacho":	"20,Aug,2021",
   "GodOfBewty":	"2,Sep,2021",
   "Going2kms":	"22,Jan,2022",
   "GOOGOOGAHGA":	"24,Jan,2022",
   "Gordii B":	"13,Nov,2021",
   "Gordi B":	"23,Aug,2021",
   "Go Outdoors":	"28,May,2021",
   "Grarorc":	"5,Aug,2021",
   "Grimmlie":	"6,Jul,2021",
   "guanaco73":	"14,Dec,2021",
   "Gz Worker":	"26,Jan,2022",
   "Hazel":	"5,Mar,2022",
   "hc b0ngz":	"24,Jan,2022",
   "HeavyGaymer":	"15,Apr,2022",
   "HeavyPair":	"9,Dec,2021",
   "Hedw1g":	"13,Aug,2021",
   "Helsper":	"7,Jan,2022",
   "Hemmur":	"3,Apr,2022",
   "Htagg":	"22,Nov,2021",
   "Humbabe":	"12,Mar,2022",
   "iamnotawook":	"30,Jan,2022",
   "IamNSFW":	"7,Jan,2022",
   "ImAKyle":	"8,Jan,2022",
   "ImZenithxian":	"25,Nov,2021",
   "im not jotwe":	"5,Oct,2021",
   "Im star":	"28,Oct,2021",
   "Iron Poovy":	"3,Sep,2021",
   "iSwarly":	"22,Nov,2021",
   "I Fukn Suck":	"30,Nov,2021",
   "Jdaws":	"13,Feb,2022",
   "JetpackDuck":	"20,Mar,2022",
   "JhowNiby":	"22,Sep,2021",
   "Jotwe":	"21,Aug,2021",
   "Jotwexd":	"19,Nov,2021",
   "Jw X":	"19,Aug,2021",
   "Jw Y":	"5,Oct,2021",
   "J R O D xD":	"13,Jan,2022",
   "K8iee":	"27,Nov,2021",
   "Kazussy":	"7,Oct,2021",
   "KELA Ari":	"2,Jan,2022",
   "Kelvino Tile":	"17,Nov,2021",
   "kermitFall":	"29,Dec,2021",
   "Kerpies":	"12,Jan,2022",
   "kilmahri":	"25,Jul,2021",
   "kleptoo":	"15,Jul,2021",
   "Koxn":	"22,Jan,2022",
   "KQLaugh":	"27,Jul,2021",
   "Krapinschitz":	"13,Dec,2021",
   "K DoubleU":	"19,Sep,2021",
   "K netty":	"17,Aug,2021",
   "L0wrey":	"3,Jan,2022",
   "L9 BOMBERMAN":	"1,May,2022",
   "lakeDerp 7":	"29,Dec,2021",
   "Laukaqe":	"23,Oct,2021",
   "lau r en":	"3,Nov,2021",
   "Leiksa":	"1,Sep,2021",
   "Leykos":	"10,Sep,2021",
   "lil brainy":	"30,Sep,2021",
   "Lil Cressant":	"25,Sep,2021",
   "Lil Hoka":	"17,Aug,2021",
   "Lil J RO D":	"12,Apr,2022",
   "LogDog Chad":	"27,Nov,2021",
   "Log Dog":	"29,Aug,2021",
   "Lqd":	"27,Nov,2021",
   "LstHcStatus":	"23,Aug,2021",
   "Lusitropy":	"20,Dec,2021",
   "Magic Clicks":	"7,Oct,2021",
   "Markszyy":	"6,Feb,2022",
   "Matholemeu":	"18,Apr,2022",
   "Matty Bob":	"18,Feb,2022",
   "Matty Bobby":	"11,Jan,2022",
   "Mayakanai 65":	"22,Oct,2021",
   "McGripped":	"17,Aug,2021",
   "McRip":	"2,Dec,2021",
   "Melanchole":	"15,Aug,2021",
   "Mentor":	"30,Dec,2021",
   "Method Zulu":	"23,Oct,2021",
   "mfBobbyHill":	"13,Sep,2021",
   "mfHank Hill":	"6,Nov,2021",
   "Mierowo":	"19,Dec,2021",
   "MindG mes":	"27,Nov,2021",
   "Mini Jrod":	"7,Sep,2021",
   "MJ23":	"26,Dec,2021",
   "MK6R":	"28,Aug,2021",
   "Mk9R":	"1,Jan,2022",
   "Moni Munch":	"22,Aug,2021",
   "monkeybisz":	"27,Nov,2021",
   "monkeybiszns":	"3,Mar,2022",
   "MopeSolo":	"7,Jan,2022",
   "MrTagMe":	"10,Aug,2021",
   "Mr Easyscape":	"1,May,2022",
   "Mr Pita":	"15,Apr,2022",
   "Nacho Alt":	"26,Jan,2022",
   "naveedd":	"16,Nov,2021",
   "Navillen":	"29,Oct,2021",
   "Na sa":	"19,Nov,2021",
   "Nex Bad":	"14,Nov,2021",
   "Nikun":	"28,May,2021",
   "nmz closed":	"29,Dec,2021",
   "nosans":	"28,May,2021",
   "Nosevesey":	"2,May,2022",
   "NoTankWicked":	"24,Mar,2022",
   "Not a Lime":	"28,May,2021",
   "Not Dre":	"30,Nov,2021",
   "Not In Love":	"28,Jul,2021",
   "Noxifer Nino":	"21,Feb,2022",
   "Nxveed":	"20,Aug,2021",
   "Occy":	"12,Feb,2022",
   "Occ y":	"2,Jan,2022",
   "oWagz":	"26,Nov,2021",
   "Paak":	"1,May,2022",
   "Pantera Form":	"30,Dec,2021",
   "PaperClip84":	"18,Aug,2021",
   "Pelco":	"4,Sep,2021",
   "pepeLzyzzPls":	"23,Jan,2022",
   "Peppey":	"7,Jan,2022",
   "Pet Awow":	"26,Nov,2021",
   "Pet Awowogei":	"16,Feb,2022",
   "PogGaymer69":	"27,Apr,2022",
   "Poovs":	"22,Feb,2022",
   "Potatohh":	"26,Nov,2021",
   "Praynr":	"11,Aug,2021",
   "Priestess":	"5,Sep,2021",
   "Priimii":	"17,Nov,2021",
   "Purell":	"15,Aug,2021",
   "P ixe l":	"27,Nov,2021",
   "QRcoding":	"11,Feb,2022",
   "Qute Catgirl":	"9,Oct,2021",
   "ratlot":	"28,Aug,2021",
   "Ratty Rat":	"31,Dec,2021",
   "Rdy4shamans":	"29,Nov,2021",
   "reluf":	"30,Nov,2021",
   "Ridgewood":	"22,Jan,2022",
   "Rng Curse":	"13,Nov,2021",
   "Rockford":	"29,Dec,2021",
   "Ryanster222":	"6,May,2022",
   "Schretty":	"28,Nov,2021",
   "Scritchh":	"27,Nov,2021",
   "ScritchhLite":	"26,Jan,2022",
   "sc a rlett":	"26,Oct,2021",
   "Seek":	"13,Jan,2022",
   "ShadowwHD":	"13,Aug,2021",
   "ShiaLaBuff":	"30,Nov,2021",
   "shkoBotnica":	"29,Dec,2021",
   "Sick Irony":	"8,Sep,2021",
   "Sid":	"6,Mar,2022",
   "siizzled":	"22,Oct,2021",
   "Skate Skrt":	"28,Nov,2021",
   "skeedush":	"17,Nov,2021",
   "Skrethan":	"28,May,2021",
   "SlayForJoy":	"18,Sep,2021",
   "Slibbon":	"9,Mar,2022",
   "Smol bwain":	"5,Dec,2021",
   "So":	"23,Mar,2022",
   "Solo Homiee":	"5,Dec,2021",
   "Solo Mourne":	"30,Nov,2021",
   "Sonuruss":	"22,Mar,2022",
   "Stokers Can":	"17,Nov,2021",
   "Strykxout":	"30,Jan,2022",
   "Strykxr":	"28,Mar,2022",
   "SullivanKing":	"23,Aug,2021",
   "S avy":	"16,Mar,2022",
   "Tatted T-Y":	"8,Aug,2021",
   "Teh Brophy":	"30,Nov,2021",
   "Teletubee":	"14,Mar,2022",
   "Terpedout":	"28,May,2021",
   "ThatOneTiger":	"29,Jan,2022",
   "This Key":	"26,Dec,2021",
   "throat queen":	"23,Dec,2021",
   "Throw Gas":	"2,Dec,2021",
   "thurcoGoose":	"22,Dec,2021",
   "Trickyish":	"3,Dec,2021",
   "Turnt":	"4,Dec,2021",
   "T agMe":	"1,Feb,2022",
   "T ile":	"8,Feb,2022",
   "uberspybwana":	"13,Nov,2021",
   "uBwana":	"28,May,2021",
   "Virg n":	"17,Apr,2022",
   "Void Sword":	"15,Nov,2021",
   "Vrzn":	"26,Apr,2022",
   "widebwana":	"13,Nov,2021",
   "Wiz That Guy":	"30,Dec,2021",
   "Wollbert":	"17,Sep,2021",
   "Wooli":	"11,Mar,2022",
   "Worldclaimed":	"2,Dec,2021",
   "W aders":	"30,Dec,2021",
   "W ays":	"28,May,2021",
   "x86":	"28,May,2021",
   "xDope Binge":	"15,Nov,2021",
   "Xuin":	"15,Nov,2021",
   "x 68":	"16,Nov,2021",
   "Yannakin":	"15,Apr,2022",
   "YeBankWicked":	"5,May,2022",
   "Yezza":	"14,Sep,2021",
   "yuulia":	"21,Aug,2021",
   "Zandles":	"18,Feb,2022",
   "zawho":	"7,Sep,2021",
   "Zaytt":	"22,Nov,2021",
   "Zolo Zoxy":	"10,Apr,2022",
   "Zorin":	"28,May,2021",
   "Zuk This":	"2,Apr,2022",
   "Z ev":	"23,Dec,2021"
}

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

  # LIST IGN
  @commands.command(hidden=True)
  async def listigns(self,ctx):
    
    global ign_list

    output_msg = ""
    
    for ign, startdate in ign_list.items():
      datestart = startdate.replace(",", " ")
      d = datetime.strptime(datestart, '%d %b %Y')
      output_msg += ign + " - " + d.strftime('%d %b %Y') + "\n"


    embed = discord.Embed(
      title = "IGN List",
      description = output_msg
    )

    print(output_msg)
    await ctx.send(embed=embed)
  
  @commands.command(hidden=True)
  async def listactive(self,ctx):
    
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

          if(excluded == False and member.bot == False and active == True):
            
            print(member)   
            list += str(member) + " - Active: " + str(active) + "\n"  
    
    embed = discord.Embed(
          title = "Log Dog ACTIVE Member List",
          description = list
        )

    await ctx.send(embed=embed)
    
    
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