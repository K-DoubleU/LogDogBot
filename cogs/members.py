import discord
from discord.ext import commands
from replit import db
import random
import time
from discord.ext.commands import cooldown, BucketType
import typing
import datetime
from discord.utils import get
import asyncio


"""
1-2 bandos
2-4 zaros
4-6 arma
6-9 zammy
9-12 sara
12-16 guth
16+ seren
"""

# create global ign list
ign_list = [
  { "name" : "02 my waifu",	"startdate" : "9-Mar-2022",	"discid" : "264592464126410762"},
  { "name" : "0nuzq",	"startdate" : "29-May-2021",	"discid" : "empty"},
  { "name" : "1 A N D 1",	"startdate" : "10-Oct-2021",	"discid" : "430881545029550082"},
  { "name" : "1 inv andy",	"startdate" : "9-Sep-2021",	"discid" : "empty"},
  { "name" : "340",	"startdate" : "17-Feb-2022",	"discid" : "empty"},
  { "name" : "8pocket42",	"startdate" : "21-Aug-2021",	"discid" : "877620838118068295"},
  { "name" : "A_SeaTurtle",	"startdate" : "1-May-2022",	"discid" : "206689272563105792"},
  { "name" : "Aceinthewhat",	"startdate" : "13-Sep-2021",	"discid" : "334223338601971712"},
  { "name" : "aGamerGaming",	"startdate" : "4-Sep-2021",	"discid" : "498953742029160459"},
  { "name" : "Agent Clank",	"startdate" : "30-May-2021",	"discid" : "396742344193343499"},
  { "name" : "AhaShakes",	"startdate" : "7-Jul-2021",	"discid" : "521356313264128000"},
  { "name" : "Alexmaee / dombcat",	"startdate" : "28-May-2021",	"discid" : "501407498717233154"},
  { "name" : "ali airball",	"startdate" : "5-Oct-2021",	"discid" : "149991011391635456"},
  { "name" : "Anjru",	"startdate" : "29-Aug-2021",	"discid" : "325060654698332161"},
  { "name" : "AoA Entei",	"startdate" : "26-Aug-2021",	"discid" : "112655954784374784"},
  { "name" : "Apepoc",	"startdate" : "23-Jun-2021",	"discid" : "212621990161285120"},
  { "name" : "arrg you srs",	"startdate" : "29-Dec-2021",	"discid" : "empty"},
  { "name" : "Atypia",	"startdate" : "5-Feb-2022",	"discid" : "295430566528942101"},
  { "name" : "avrg",	"startdate" : "22-Aug-2021",	"discid" : "512051411358318612"},
  { "name" : "Bacoid1",	"startdate" : "13-Jan-2022",	"discid" : "119812671657869314"},
  { "name" : "BAMB0NG",	"startdate" : "31-Jan-2022",	"discid" : "623951324035285016"},
  { "name" : "bee safe",	"startdate" : "3-Jun-2021",	"discid" : "142373764729012228"},
  { "name" : "BlendingTime",	"startdate" : "28-May-2021",	"discid" : "894376531101642844"},
  { "name" : "boile y",	"startdate" : "22-Feb-2022",	"discid" : "267351990265315328"},
  { "name" : "boobs420",	"startdate" : "9-Mar-2022",	"discid" : "478056570215727105"},
  { "name" : "Born Soft",	"startdate" : "3-Feb-2022",	"discid" : "empty"},
  { "name" : "Bow And K0",	"startdate" : "9-Jan-2022",	"discid" : "378788239156183041"},
  { "name" : "bo bby",	"startdate" : "12-Oct-2021",	"discid" : "391049478909460481"},
  { "name" : "Brando Jamz",	"startdate" : "12-Jan-2022",	"discid" : "578342900652441600"},
  { "name" : "brutwoburst",	"startdate" : "21-Nov-2021",	"discid" : "empty"},
  { "name" : "Bubblenab",	"startdate" : "28-May-2021",	"discid" : "242758170202603520"},
  { "name" : "BUD LlGHTS",	"startdate" : "17-Aug-2021",	"discid" : "331158863543795714"},
  { "name" : "buying 2x P",	"startdate" : "7-Feb-2022",	"discid" : "186385846608461824"},
  { "name" : "b oe",	"startdate" : "3-Feb-2022",	"discid" : "339199480249450496"},
  { "name" : "b rfb",	"startdate" : "29-Oct-2021",	"discid" : "553385419820236810"},
  { "name" : "Capn Tj",	"startdate" : "20-Aug-2021",	"discid" : "517561182941347863"},
  { "name" : "Caring",	"startdate" : "1-Jan-2022",	"discid" : "564827382007988248"},
  { "name" : "Cerastease",	"startdate" : "2-Nov-2021",	"discid" : "empty"},
  { "name" : "Chasx",	"startdate" : "20-Aug-2021",	"discid" : "444511836549808148"},
  { "name" : "ChefBoyArtyy",	"startdate" : "7-Jan-2022",	"discid" : "355946073916833793"},
  { "name" : "Chronology",	"startdate" : "29-Dec-2021",	"discid" : "745156228698603531"},
  { "name" : "ClaasJaguar",	"startdate" : "18-Dec-2021",	"discid" : "790346784827506688"},
  { "name" : "ClassyWizKey",	"startdate" : "21-Oct-2021",	"discid" : "441752954475773973"},
  { "name" : "Clipper",	"startdate" : "12-Feb-2022",	"discid" : "176153878037921792"},
  { "name" : "cloud zen",	"startdate" : "16-Nov-2021",	"discid" : "970353859866267720"},
  { "name" : "Coitle",	"startdate" : "10-May-2022",	"discid" : "426519479531470849"},
  { "name" : "Consistent C",	"startdate" : "2-Mar-2022",	"discid" : "321142937008209920"},
  { "name" : "coxieDino",	"startdate" : "15-Aug-2021",	"discid" : "439579576956354561"},
  { "name" : "Cp Teemo",	"startdate" : "28-May-2021",	"discid" : "147159822674952192"},
  { "name" : "CrimsonGFX",	"startdate" : "8-Jan-2022",	"discid" : "139953665766064128"},
  { "name" : "cupma",	"startdate" : "26-Aug-2021",	"discid" : "79376430823116800"},
  { "name" : "C himera",	"startdate" : "3-Jan-2022",	"discid" : "363061303843225600"},
  { "name" : "c h u c kles",	"startdate" : "21-Aug-2021",	"discid" : "353675228464807946"},
  { "name" : "C L Y",	"startdate" : "28-May-2021",	"discid" : "595484476155625474"},
  { "name" : "C olbby",	"startdate" : "10-Jul-2021",	"discid" : "564846131109036055"},
  { "name" : "Darkrise",	"startdate" : "24-Aug-2021",	"discid" : "empty"},
  { "name" : "DatNeck",	"startdate" : "28-May-2021",	"discid" : "252465779650461697"},
  { "name" : "Deli Barista",	"startdate" : "30-Dec-2021",	"discid" : "935882692065636352"},
  { "name" : "Deli Cashier",	"startdate" : "31-Dec-2021",	"discid" : "257989333368176640"},
  { "name" : "Delystt",	"startdate" : "23-Aug-2021",	"discid" : "166337767188594690"},
  { "name" : "Doodstil",	"startdate" : "20-Nov-2021",	"discid" : "empty"},
  { "name" : "Dorvagten",	"startdate" : "26-Apr-2022",	"discid" : "231113059643424769"},
  { "name" : "Do It Myself",	"startdate" : "27-Nov-2021",	"discid" : "215554024206761984"},
  { "name" : "Dreww",	"startdate" : "20-Dec-2021",	"discid" : "138171478309863424"},
  { "name" : "dxamfetamine",	"startdate" : "3-Dec-2021",	"discid" : "empty"},
  { "name" : "D o n s o n",	"startdate" : "21-Aug-2021",	"discid" : "298845668301209602"},
  { "name" : "EarthNoGlobe",	"startdate" : "24-Nov-2021",	"discid" : "empty"},
  { "name" : "Elwood",	"startdate" : "18-Feb-2022",	"discid" : "empty"},
  { "name" : "enzo_O",	"startdate" : "28-Jan-2022",	"discid" : "364455320837160971"},
  { "name" : "eVirgin",	"startdate" : "30-Jan-2022",	"discid" : "138841636183605248"},
  { "name" : "Mr Easyscape / Ez 4 Easy",	"startdate" : "27-Dec-2021",	"discid" : "232507005623992320"},
  { "name" : "FAILED ZEUS",	"startdate" : "22-Aug-2021",	"discid" : "201597280577388544"},
  { "name" : "FDM",	"startdate" : "23-Oct-2021",	"discid" : "272115473771003904"},
  { "name" : "fe iris",	"startdate" : "8-Jan-2022",	"discid" : "267019606936387605"},
  { "name" : "Fe Maui",	"startdate" : "1-Dec-2021",	"discid" : "empty"},
  { "name" : "Fioriture",	"startdate" : "26-Jan-2022",	"discid" : "97545813269413888"},
  { "name" : "Gerglidor",	"startdate" : "19-Dec-2021",	"discid" : "266429962570039297"},
  { "name" : "Gewnster",	"startdate" : "12-Jul-2021",	"discid" : "358080297297903616"},
  { "name" : "GIM902RANGER",	"startdate" : "7-Jan-2022",	"discid" : "506709347577888779"},
  { "name" : "GIMitalia",	"startdate" : "15-Nov-2021",	"discid" : "161528347753578497"},
  { "name" : "GlizzyL",	"startdate" : "31-Dec-2021",	"discid" : "126057299457343488"},
  { "name" : "Globe Denier",	"startdate" : "2-Nov-2021",	"discid" : "266326617322684419"},
  { "name" : "Gmar",	"startdate" : "1-Sep-2021",	"discid" : "512051411358318612"},
  { "name" : "Gnarly Nacho",	"startdate" : "20-Aug-2021",	"discid" : "590042325170782209"},
  { "name" : "GodOfBewty",	"startdate" : "2-Sep-2021",	"discid" : "176424721104109568"},
  { "name" : "Going2kms",	"startdate" : "22-Jan-2022",	"discid" : "210229094585991169"},
  { "name" : "Gordi B",	"startdate" : "23-Aug-2021",	"discid" : "148962478418690048"},
  { "name" : "Go Outdoors",	"startdate" : "28-May-2021",	"discid" : "544670657582071810"},
  { "name" : "Grimmlie",	"startdate" : "6-Jul-2021",	"discid" : "243541005721141249"},
  { "name" : "guanaco73",	"startdate" : "14-Dec-2021",	"discid" : "266666482841157632"},
  { "name" : "Hazel",	"startdate" : "5-Mar-2022",	"discid" : "431667028936491010"},
  { "name" : "HeavyGaymer",	"startdate" : "15-Apr-2022",	"discid" : "empty"},
  { "name" : "HeavyPair",	"startdate" : "9-Dec-2021",	"discid" : "249003289457197057"},
  { "name" : "Hedw1g",	"startdate" : "13-Aug-2021",	"discid" : "empty"},
  { "name" : "Helsper",	"startdate" : "7-Jan-2022",	"discid" : "229402998135193601"},
  { "name" : "Hemmur",	"startdate" : "23-Dec-2021",	"discid" : "241804361913597952"},
  { "name" : "Htagg",	"startdate" : "22-Nov-2021",	"discid" : "empty"},
  { "name" : "Humbabe",	"startdate" : "12-Mar-2022",	"discid" : "220077618085625856"},
  { "name" : "iamnotawook",	"startdate" : "30-Jan-2022",	"discid" : "360269595506114561"},
  { "name" : "IamNSFW",	"startdate" : "7-Jan-2022",	"discid" : "244186443344379905"},
  { "name" : "ImAKyle",	"startdate" : "8-Jan-2022",	"discid" : "302210795289182210"},
  { "name" : "ImZenithxian",	"startdate" : "25-Nov-2021",	"discid" : "151041083134967808"},
  { "name" : "Im star",	"startdate" : "28-Oct-2021",	"discid" : "114797077166292996"},
  { "name" : "Iron Poovy / Poovs",	"startdate" : "3-Sep-2021",	"discid" : "269179149858504714"},
  { "name" : "iSwarly",	"startdate" : "22-Nov-2021",	"discid" : "283040876702203905"},
  { "name" : "I Fukn Suck",	"startdate" : "30-Nov-2021",	"discid" : "219336107073077248"},
  { "name" : "Jdaws",	"startdate" : "13-Feb-2022",	"discid" : "186728270002257921"},
  { "name" : "JetpackDuck",	"startdate" : "20-Mar-2022",	"discid" : "351048069258936320"},
  { "name" : "JhowNiby",	"startdate" : "22-Sep-2021",	"discid" : "empty"},
  { "name" : "Jotwe",	"startdate" : "21-Aug-2021",	"discid" : "101685677745266688"},
  { "name" : "Jw X",	"startdate" : "19-Aug-2021",	"discid" : "110889810524184576"},
  { "name" : "J R O D xD",	"startdate" : "1-Oct-2021",	"discid" : "235564731685928970"},
  { "name" : "K8iee",	"startdate" : "27-Nov-2021",	"discid" : "426239904545112065"},
  { "name" : "KELA Ari",	"startdate" : "2-Jan-2022",	"discid" : "361260774020349954"},
  { "name" : "Kelvino Tile",	"startdate" : "17-Nov-2021",	"discid" : "438471390224711680"},
  { "name" : "kermitFall",	"startdate" : "29-Dec-2021",	"discid" : "empty"},
  { "name" : "Kerpies",	"startdate" : "12-Jan-2022",	"discid" : "345292683146821636"},
  { "name" : "kilmahri",	"startdate" : "25-Jul-2021",	"discid" : "582268739844833290"},
  { "name" : "kleptoo",	"startdate" : "15-Jul-2021",	"discid" : "385731467327569921"},
  { "name" : "KQLaugh",	"startdate" : "27-Jul-2021",	"discid" : "91274323351834624"},
  { "name" : "Krapinschitz",	"startdate" : "13-Dec-2021",	"discid" : "275136744784003074"},
  { "name" : "K DoubleU",	"startdate" : "19-Sep-2021",	"discid" : "300861348546347010"},
  { "name" : "K netty",	"startdate" : "17-Aug-2021",	"discid" : "152409542662029312"},
  { "name" : "L0wrey",	"startdate" : "3-Jan-2022",	"discid" : "457176597439578112"},
  { "name" : "L9 BOMBERMAN",	"startdate" : "1-May-2022",	"discid" : "108042168593039360"},
  { "name" : "Laukaqe",	"startdate" : "23-Oct-2021",	"discid" : "336092190122180608"},
  { "name" : "lau r en",	"startdate" : "3-Nov-2021",	"discid" : "303349359385378816"},
  { "name" : "Leiksa",	"startdate" : "1-Sep-2021",	"discid" : "empty"},
  { "name" : "Leykos",	"startdate" : "10-Sep-2021",	"discid" : "494220442891059253"},
  { "name" : "lil brainy / smol bwain",	"startdate" : "30-Sep-2021",	"discid" : "315150812508585986"},
  { "name" : "Lil Hoka",	"startdate" : "17-Aug-2021",	"discid" : "396938266739343362"},
  { "name" : "LogDog Chad",	"startdate" : "27-Nov-2021",	"discid" : "227951545977667584"},
  { "name" : "Log Dog",	"startdate" : "29-Aug-2021",	"discid" : "empty"},
  { "name" : "Lqd",	"startdate" : "27-Nov-2021",	"discid" : "empty"},
  { "name" : "LstHcStatus",	"startdate" : "23-Aug-2021",	"discid" : "empty"},
  { "name" : "Lusitropy",	"startdate" : "20-Dec-2021",	"discid" : "386198987343921163"},
  { "name" : "Magic Clicks",	"startdate" : "7-Oct-2021",	"discid" : "267897767572013056"},
  { "name" : "Markszyy",	"startdate" : "6-Feb-2022",	"discid" : "345325893863866368"},
  { "name" : "Matholemeu",	"startdate" : "18-Apr-2022",	"discid" : "307611991466573834"},
  { "name" : "Matty Bobby",	"startdate" : "11-Jan-2022",	"discid" : "195417287774306315"},
  { "name" : "Mayakanai 65",	"startdate" : "22-Oct-2021",	"discid" : "144633126847512577"},
  { "name" : "McGripped",	"startdate" : "17-Aug-2021",	"discid" : "384619294518018049"},
  { "name" : "Melanchole",	"startdate" : "15-Aug-2021",	"discid" : "254058474344939520"},
  { "name" : "Mentor",	"startdate" : "30-Dec-2021",	"discid" : "786744399454535731"},
  { "name" : "mfBobbyHill",	"startdate" : "13-Sep-2021",	"discid" : "229750942709317632"},
  { "name" : "Mierowo",	"startdate" : "19-Dec-2021",	"discid" : "138481848362860553"},
  { "name" : "MindG mes",	"startdate" : "27-Nov-2021",	"discid" : "470719970536587274"},
  { "name" : "MJ23",	"startdate" : "26-Dec-2021",	"discid" : "187331981430751232"},
  { "name" : "MK6R",	"startdate" : "28-Aug-2021",	"discid" : "260255972465836033"},
  { "name" : "Mk9R",	"startdate" : "1-Jan-2022",	"discid" : "217468124700606464"},
  { "name" : "monkeybisz",	"startdate" : "27-Nov-2021",	"discid" : "746723596243697694"},
  { "name" : "MopeSolo",	"startdate" : "7-Jan-2022",	"discid" : "220274809941000192"},
  { "name" : "MrTagMe",	"startdate" : "10-Aug-2021",	"discid" : "577183120378298389"},
  { "name" : "Mr Pita",	"startdate" : "15-Apr-2022",	"discid" : "172419546206961664"},
  { "name" : "Navillen",	"startdate" : "29-Oct-2021",	"discid" : "240125024814628865"},
  { "name" : "Na sa",	"startdate" : "19-Nov-2021",	"discid" : "empty"},
  { "name" : "Nex Bad",	"startdate" : "14-Nov-2021",	"discid" : "973036248409202718"},
  { "name" : "Nikun",	"startdate" : "28-May-2021",	"discid" : "135470450380636161"},
  { "name" : "nmz closed",	"startdate" : "29-Dec-2021",	"discid" : "empty"},
  { "name" : "nosans",	"startdate" : "28-May-2021",	"discid" : "513591452685565997"},
  { "name" : "Nosevesey",	"startdate" : "2-May-2022",	"discid" : "222424859450277888"},
  { "name" : "NoTankWicked",	"startdate" : "24-Mar-2022",	"discid" : "155344610980265984"},
  { "name" : "Not a Lime",	"startdate" : "28-May-2021",	"discid" : "355643068344434688"},
  { "name" : "Not Dre",	"startdate" : "30-Nov-2021",	"discid" : "532962255025995777"},
  { "name" : "Not In Love / Hc B0ngz",	"startdate" : "28-Jul-2021",	"discid" : "317488864002441228"},
  { "name" : "Nxveed",	"startdate" : "20-Aug-2021",	"discid" : "270316202134470656"},
  { "name" : "Occ y",	"startdate" : "2-Jan-2022",	"discid" : "280131544654544897"},
  { "name" : "oWagz",	"startdate" : "26-Nov-2021",	"discid" : "302251346709446657"},
  { "name" : "PaperClip84",	"startdate" : "18-Aug-2021",	"discid" : "102558149067689984"},
  { "name" : "Pelco",	"startdate" : "4-Sep-2021",	"discid" : "265964447003181060"},
  { "name" : "pepeLzyzzPls",	"startdate" : "23-Jan-2022",	"discid" : "172946261870116864"},
  { "name" : "Peppey",	"startdate" : "7-Jan-2022",	"discid" : "231372376410030080"},
  { "name" : "Pet Awowogei",	"startdate" : "26-Nov-2021",	"discid" : "480406918842810378"},
  { "name" : "PogGaymer69",	"startdate" : "27-Apr-2022",	"discid" : "331892929511555072"},
  { "name" : "Potatohh",	"startdate" : "26-Nov-2021",	"discid" : "149004210413895680"},
  { "name" : "Praynr",	"startdate" : "11-Aug-2021",	"discid" : "197140022569205762"},
  { "name" : "Priestess",	"startdate" : "5-Sep-2021",	"discid" : "148666266499022848"},
  { "name" : "Priimii",	"startdate" : "17-Nov-2021",	"discid" : "430768104667217920"},
  { "name" : "Purell",	"startdate" : "15-Aug-2021",	"discid" : "102825169688461312"},
  { "name" : "P ixe l",	"startdate" : "27-Nov-2021",	"discid" : "152084482600599552"},
  { "name" : "QRcoding",	"startdate" : "11-Feb-2022",	"discid" : "153287234714337281"},
  { "name" : "Qute Catgirl",	"startdate" : "9-Oct-2021",	"discid" : "172398511139061761"},
  { "name" : "ratlot",	"startdate" : "28-Aug-2021",	"discid" : "416005932506677248"},
  { "name" : "Rdy4shamans",	"startdate" : "29-Nov-2021",	"discid" : "empty"},
  { "name" : "reluf",	"startdate" : "30-Nov-2021",	"discid" : "90644146921963520"},
  { "name" : "Ridgewood",	"startdate" : "22-Jan-2022",	"discid" : "286930944907018243"},
  { "name" : "Rng Curse",	"startdate" : "13-Nov-2021",	"discid" : "343047708766109696"},
  { "name" : "Rockford",	"startdate" : "29-Dec-2021",	"discid" : "186889463757144064"},
  { "name" : "Ryanster222",	"startdate" : "6-May-2022",	"discid" : "313376214054207488"},
  { "name" : "Schretty",	"startdate" : "28-Nov-2021",	"discid" : "594611292996894751"},
  { "name" : "Scritchh",	"startdate" : "27-Nov-2021",	"discid" : "273322064457367552"},
  { "name" : "sc a rlett",	"startdate" : "26-Oct-2021",	"discid" : "98468167289966592"},
  { "name" : "Seek",	"startdate" : "13-Jan-2022",	"discid" : "184404573744529410"},
  { "name" : "ShadowwHD",	"startdate" : "13-Aug-2021",	"discid" : "406316359056883725"},
  { "name" : "ShiaLaBuff",	"startdate" : "30-Nov-2021",	"discid" : "576595374840479745"},
  { "name" : "shkoBotnica",	"startdate" : "29-Dec-2021",	"discid" : "248795510540861441"},
  { "name" : "Sid",	"startdate" : "6-Mar-2022",	"discid" : "236224288074629130"},
  { "name" : "siizzled",	"startdate" : "22-Oct-2021",	"discid" : "empty"},
  { "name" : "Skate Skrt",	"startdate" : "28-Nov-2021",	"discid" : "180033534675648512"},
  { "name" : "skeedush",	"startdate" : "17-Nov-2021",	"discid" : "279393071295365120"},
  { "name" : "Skrethan",	"startdate" : "28-May-2021",	"discid" : "354409159275577346"},
  { "name" : "SlayForJoy",	"startdate" : "18-Sep-2021",	"discid" : "199654276052549632"},
  { "name" : "Slibbon",	"startdate" : "9-Mar-2022",	"discid" : "125098939975335937"},
  { "name" : "So",	"startdate" : "23-Mar-2022",	"discid" : "284085570198568961"},
  { "name" : "Solo Homiee",	"startdate" : "5-Dec-2021",	"discid" : "114956191544639490"},
  { "name" : "Solo Mourne",	"startdate" : "30-Nov-2021",	"discid" : "empty"},
  { "name" : "Sonuruss",	"startdate" : "22-Mar-2022",	"discid" : "161679594754146305"},
  { "name" : "Stokers Can",	"startdate" : "17-Nov-2021",	"discid" : "350769708481642496"},
  { "name" : "Strykxout",	"startdate" : "30-Jan-2022",	"discid" : "518909166236991489"},
  { "name" : "SullivanKing",	"startdate" : "23-Aug-2021",	"discid" : "empty"},
  { "name" : "Tatted T-Y",	"startdate" : "8-Aug-2021",	"discid" : "254047410118983680"},
  { "name" : "Teh Brophy",	"startdate" : "30-Nov-2021",	"discid" : "250503565116833792"},
  { "name" : "Teletubee",	"startdate" : "14-Mar-2022",	"discid" : "655493098901602315"},
  { "name" : "Terpedout",	"startdate" : "28-May-2021",	"discid" : "268672512148242436"},
  { "name" : "ThatOneTiger",	"startdate" : "29-Jan-2022",	"discid" : "104295371164913664"},
  { "name" : "This Key",	"startdate" : "26-Dec-2021",	"discid" : "282593884599746561"},
  { "name" : "throat queen",	"startdate" : "23-Dec-2021",	"discid" : "210478979730112513"},
  { "name" : "Throw Gas",	"startdate" : "2-Dec-2021",	"discid" : "empty"},
  { "name" : "thurcoGoose",	"startdate" : "22-Dec-2021",	"discid" : "197897020235579392"},
  { "name" : "Trickyish",	"startdate" : "3-Dec-2021",	"discid" : "167405334955163648"},
  { "name" : "Turnt",	"startdate" : "4-Dec-2021",	"discid" : "221791020298403842"},
  { "name" : "T ile / Coolchub",	"startdate" : "8-Feb-2022",	"discid" : "206295238606716928"},
  { "name" : "uberspybwana / widebwana",	"startdate" : "13-Nov-2021",	"discid" : "153350580125827072"},
  { "name" : "uBwana",	"startdate" : "28-May-2021",	"discid" : "350873366728540161"},
  { "name" : "Void Sword",	"startdate" : "15-Nov-2021",	"discid" : "286337940290928642"},
  { "name" : "Volkert",	"startdate" : "24-Aug-2021",	"discid" : "291281340035235841"},
  { "name" : "Wollbert",	"startdate" : "17-Sep-2021",	"discid" : "233233338217791489"},
  { "name" : "Wooli",	"startdate" : "11-Mar-2022",	"discid" : "267140229381619712"},
  { "name" : "Worldclaimed",	"startdate" : "2-Dec-2021",	"discid" : "534781635594551296"},
  { "name" : "W aders",	"startdate" : "30-Dec-2021",	"discid" : "448231666025103370"},
  { "name" : "W ays",	"startdate" : "28-May-2021",	"discid" : "178547737048907776"},
  { "name" : "x86",	"startdate" : "28-May-2021",	"discid" : "145611584381648897"},
  { "name" : "xDope Binge",	"startdate" : "15-Nov-2021",	"discid" : "428768002222194688"},
  { "name" : "Yannakin",	"startdate" : "15-Apr-2022",	"discid" : "278769492262125569"},
  { "name" : "Yezza",	"startdate" : "14-Sep-2021",	"discid" : "247468465483546624"},
  { "name" : "yuulia",	"startdate" : "21-Aug-2021",	"discid" : "82204014317408256"},
  { "name" : "zawho",	"startdate" : "7-Sep-2021",	"discid" : "241037329408458752"},
  { "name" : "Zaytt",	"startdate" : "22-Nov-2021",	"discid" : "204321993825189889"},
  { "name" : "Zolo Zoxy",	"startdate" : "10-Apr-2022",	"discid" : "226380140949667840"},
  { "name" : "Zuk This",	"startdate" : "2-Apr-2022",	"discid" : "120539364802560001"},
  { "name" : "Testing",	"startdate" : "2-Jan-2020",	"discid" : "565678866237227024"},
  { "name" : "Z ev",	"startdate" : "23-Dec-2021",	"discid" : "290195127283220493"}
  
]

class Members(commands.Cog):


  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.Cog.listener()
  async def on_message(self, message):

    if message.author == self.bot.user:
      return

    if message.channel.id == 974088082401943562:
      await message.delete()

  # REMOVE CLAN COMMAND
  @commands.command(help = "Removes clan information from a specified user. You can either mention the user or type their IGN.\nExample: .removeclan @FridgeBot\nExample: .removeclan xTreeChopper69x")
  async def removeclan(self, ctx, *args):

    allowedroles = [
      discord.utils.find(lambda r: r.name == 'CEO', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Board', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Staff', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Bot Dev', ctx.message.guild.roles)
    ]

    allowed = False
    
    for role in ctx.author.roles:
      if(role in allowedroles):
        allowed = True

    if(allowed == False):
      await ctx.send("You do not have the required role(s) to use this command. Fuck off.")
      return

    embed = discord.Embed(
      title = "Clan Removal",
      description = "React with :white_check_mark: to confirm"
    )
    
    try:

      userfound = False
      
      if ("@" in args[0]):

        arg = args[0]

        
        to_remove = arg[2:20]

        print(to_remove)
        
        if(to_remove in db):
          
          if("clan" in db[to_remove]):

            userfound = True
            
            embed.add_field(
              name = "Removing:",
              value = "IGN: " + db[to_remove]["clan"]["ign"]
            )

      else:

        arg = " ".join(args[:])
        
        for user in db:

          if("clan" in db[user]):

            if(db[user]["clan"]["ign"] == arg):

              to_remove = user

              userfound = True
              
              embed.add_field(
                name = "Removing:",
                value = "IGN: " + db[user]["clan"]["ign"]
              )

      if(userfound):

        msg = await ctx.send(embed=embed)

      else:

        embed = discord.Embed(
          title = ":x: User Not Found"
        )

        await ctx.send(embed=embed)
        return

      await msg.add_reaction("✅")

      def check(reaction, person):
        
        return person == ctx.author and str(reaction.emoji) == '✅'

      try:
        
        reaction, person = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
        
      except asyncio.TimeoutError:
        
        print("timed out")

      else:

        del db[to_remove]["clan"]

        doneembed = discord.Embed(
          title = ":white_check_mark: Clan Member Removed"
        )

        await ctx.send(embed=doneembed)
        
      

    except Exception as e:

      print("ERROR HANDLING HERE\n" + str(e))
      

  @removeclan.error
  async def removeclan_error(self, ctx, error): 
    if isinstance(error, commands.BadArgument):
      
      await ctx.send('I could not find that user')

    else:
      print(error)


  # Set IGN Command
  @commands.command(help = "Sets an in-game name for a specified discord user. \nExample: '.setign @FridgeBot xTreeChopper69x'")
  async def setign(self, ctx, member: discord.Member, *args):

    allowedroles = [
      discord.utils.find(lambda r: r.name == 'CEO', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Board', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Staff', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Bot Dev', ctx.message.guild.roles)
    ]

    allowed = False
    
    for role in ctx.author.roles:
      if(role in allowedroles):
        allowed = True

    if(allowed == False):
      await ctx.send("You do not have the required role(s) to use this command. Fuck off.")
      return

    if(not args):
      await ctx.send("You must provide an IGN")
      return

    logdoggerid = 893277099350163518
    logdoggerrole = get(ctx.guild.roles, id = logdoggerid)

    await ctx.message.delete()
    
    user = str(member.id)

    arg = " ".join(args[:])

    if(user not in db):
      db[user] = {
        "bal":0,
        "bank":0
      }

    if("clan" not in db[user]):
      db[user]["clan"] = {
        "ign" : arg
      }

    else:
      db[user]["clan"]["ign"] = arg

    if(logdoggerrole not in member.roles):
      
      await member.add_roles(logdoggerrole)

    embed = discord.Embed(
      title = ":pencil: Set IGN"
    )

    embed.add_field(
      name = ":white_check_mark: IGN Set Successfully",
      value = "**User:** " + member.name + "\n**IGN:** " + arg
    )
    
    await ctx.send(embed=embed)

  # SET START DATE COMMAND
  @commands.command(help = "Sets a start date for a specified discord user. \nDate format is [Day - Month - Year]\nExample: '.setstart @FridgeBot 12-4-2022'", aliases = ["setstart"])
  async def setstartdate(self, ctx, member: discord.Member, arg = None):

    await ctx.message.delete()
    
    allowedroles = [
      discord.utils.find(lambda r: r.name == 'CEO', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Board', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Staff', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Bot Dev', ctx.message.guild.roles)
    ]

    allowed = False
    
    for role in ctx.author.roles:
      if(role in allowedroles):
        allowed = True

    if(allowed == False):
      await ctx.send("You do not have the required role(s) to use this command. Fuck off.")
      return
    
    logdoggerid = 893277099350163518
    logdoggerrole = get(ctx.guild.roles, id = logdoggerid)

    if(not arg):
      await ctx.send("You must provide a date")
      return

    user = str(member.id)

    if(user not in db):
      db[user] = {
        "clan":{}
      }

    try:

      # If arg is today, we need to make the date = today's date
      if(arg.lower() == "today"):
        
        d = datetime.datetime.now()
      
      else:
      # Split the arg so we can check for the month
        argsplit = arg.split("-")

        datestart = arg.replace("-", " ")

        if(argsplit[1].isdigit()):
          # If they entered a number for month, we handle it here
          d = datetime.datetime.strptime(datestart, '%d %m %Y')
  
        else:
  
          if(len(argsplit[1]) > 3):
            d = datetime.datetime.strptime(datestart, '%d %B %Y')
  
          else:
            d = datetime.datetime.strptime(datestart, '%d %b %Y')

      datereformat = d.strftime('%d %b %Y')
      
      datetoadd = "-".join(datereformat.split())
      
      print("date to add: " + datetoadd)

      msg_embed = "Setting **" + member.name + "'s** start date:"

      field_embed = "**Day:** " + str(d.day) + "\n**Month:** " + str(d.month) + "\n**Year:** " + str(d.year)
      
      embed = discord.Embed(
        title = ":calendar_spiral: Set Start Date",
        description = msg_embed
      )

      embed.add_field(
        name = field_embed,
        value = "React with :white_check_mark: to confirm"
      )

      msg = await ctx.send(embed=embed)

      await msg.add_reaction("✅")
      

      def check(reaction, user):
        
        return user == ctx.author and str(reaction.emoji) == '✅'

      try:
        
        reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
        
      except asyncio.TimeoutError:
        
        print("timed out")
        
      else:

        user = str(member.id)
        
        if("clan" not in db[user]):
          db[user]["clan"] = {
            "start":datetoadd
          }

        else:

          db[user]["clan"]["start"] = datetoadd

        # Set successfully
          
        await msg.delete()
        
        doneembed = discord.Embed(
          title = ":calendar_spiral: Set Start Date"
        )

        doneembed.add_field(
          name = ":white_check_mark: Start Date Set Successfully",
          value = "**User:** " + member.name + "\n" + field_embed
        )

        if(logdoggerrole not in member.roles):
          
          await member.add_roles(logdoggerrole)
          
        await ctx.send(embed=doneembed)
      
      print(d)

    except Exception as e:
      print(e)
      await ctx.send("Invalid date format. Must be 'day-month-year'")
    
    print("executed")

  # UPDATE RANK COMMAND THIS IS THE CRAZY SHIT THAT DOES ALL THE ROLE UPDATING
  @commands.command(hidden=True)
  async def updaterank(self, ctx, member: discord.Member = None):
    
    if(ctx.author.id != 332601516626280450): return

    global ign_list

    role_list = [
      894376839454269491,
      894376617999233026,
      894376531101642844,
      894376448322838558,
      894376273000955975,
      894375804874653756,
      894376017739808798
    ]

    if(member):

      user = str(member.id)

      print(member.id)
      print("member present")

      if(user not in db):
        print("user not in db")

        await ctx.send("User not found to update rank")
        return

      if("clan" not in db[user]):

        await ctx.send("This user is not in the clan!")
        return
        
      start_date = db[user]["clan"]["start"]

      datestart = start_date.replace("-", " ")
      
      d = datetime.datetime.strptime(datestart, '%d %b %Y')

      today = datetime.datetime.now()

      member_time = (today - d).days

      print(member_time)

      months = (today.year - d.year) * 12 + (today.month - d.month)

      print(months)
      
      

      if(months >= 16):
        roleid = 894376839454269491
      elif(months >= 12):
        roleid = 894376617999233026
      elif(months >= 9):
        roleid = 894376531101642844
      elif(months >= 6):
        roleid = 894376448322838558
      elif(months >= 4):
        roleid = 894376273000955975
      elif(months >= 2):
        roleid = 894375804874653756
      elif(months >= 1):
        roleid = 894376017739808798
      else:
        roleid = 894376017739808798

      # Loop through role id's
      for r in role_list:

        # store the current role from the current id in the loop
        role = get(ctx.guild.roles, id = r)

        # If the user already has this role...
        if(role in member.roles):

          #If they have the role already, we want to make sure it's the role they should have
          if(roleid != r):
            #If it's not, we remove it
            await member.remove_roles(role)

          # Otherwise, we'll add it
        else:
          if(roleid == r):
            await member.add_roles(role)
            

      roleadded = get(ctx.guild.roles, id = roleid)
      
      await ctx.send("IGN: " + db[user]["clan"]["ign"] + "\nJoined: " + start_date + "\nTime since joining: " + str(months) + " months\n" + "Role added: " + str(roleadded))
        
    else:

      for user, entries in db.items():

        if("clan" not in entries): continue

        member = ctx.guild.get_member(int(user))

        if(member is None): continue
        
        print(member)
        
        start_date = db[user]["clan"]["start"]

        datestart = start_date.replace("-", " ")
        
        d = datetime.datetime.strptime(datestart, '%d %b %Y')
  
        today = datetime.datetime.now()
  
        member_time = (today - d).days
  
        months = (today.year - d.year) * 12 + (today.month - d.month)
  
        print(months)
        
        print("Joined: " + start_date + "\nTime since joining: " + str(months) + " months")
  
        if(months >= 16):
          roleid = 894376839454269491
        elif(months >= 12):
          roleid = 894376617999233026
        elif(months >= 9):
          roleid = 894376531101642844
        elif(months >= 6):
          roleid = 894376448322838558
        elif(months >= 4):
          roleid = 894376273000955975
        elif(months >= 2):
          roleid = 894375804874653756
        elif(months >= 1):
          roleid = 894376017739808798
        else:
          roleid = 894376017739808798

        for r in role_list:

          # store the current role from the current id in the loop
          role = get(ctx.guild.roles, id = r)
  
          # If the user already has this role...
          if(role in member.roles):
            print(role)
  
            #If they have the role already, we want to make sure it's the role they should have
            if(roleid != r):
              #If it's not, we remove it
              await member.remove_roles(role)
              print("removed role")
  
            # Otherwise, we'll add it
          else:
            if(roleid == r):
              await member.add_roles(role)
              print("added role")
        
      await ctx.send("Finished. Did it work? Find out on the next episode of Dragonball Z")  
        
    print("executed")

  # GET RANKS COMMAND
  @commands.command(help = "Outputs a list of IGN's - Rank, based on their start date. This command can take up to 10 seconds to execute. Please do not spam if you don't see the list right away.")
  async def getranks(self,ctx):
    
    allowedroles = [
      discord.utils.find(lambda r: r.name == 'CEO', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Board', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Staff', ctx.message.guild.roles),
      discord.utils.find(lambda r: r.name == 'Bot Dev', ctx.message.guild.roles)
    ]

    allowed = False
    
    for role in ctx.author.roles:
      if(role in allowedroles):
        allowed = True

    if(allowed == False):
      await ctx.send("You do not have the required role(s) to use this command. Fuck off.")
      return

    output_string = ""
    output_string2 = ""
    output_string3 = ""
    
    for user, entries in db.items():

      if("clan" not in entries): continue

      start_date = db[user]["clan"]["start"]

      datestart = start_date.replace("-", " ")
      
      d = datetime.datetime.strptime(datestart, '%d %b %Y')

      today = datetime.datetime.now()

      months = (today.year - d.year) * 12 + (today.month - d.month)

      if(months >= 16):
        roleid = 894376839454269491
      elif(months >= 12):
        roleid = 894376617999233026
      elif(months >= 9):
        roleid = 894376531101642844
      elif(months >= 6):
        roleid = 894376448322838558
      elif(months >= 4):
        roleid = 894376273000955975
      elif(months >= 2):
        roleid = 894375804874653756
      elif(months >= 1):
        roleid = 894376017739808798
      else:
        roleid = 894376017739808798

      roleadded = get(ctx.guild.roles, id = roleid)

      if(len(output_string) < 3900):
        output_string += db[user]["clan"]["ign"] + " - " + str(roleadded) + "\n"

      elif(len(output_string2) < 3900):
        output_string2 += db[user]["clan"]["ign"] + " - " + str(roleadded) + "\n"

      elif(len(output_string3) < 3900):
        output_string3 += db[user]["clan"]["ign"] + " - " + str(roleadded) + "\n"


    embed = discord.Embed(
      title = "IGN - RANK (Page 1)",
      description = output_string
    )

    embed2 = discord.Embed(
      title = "IGN - RANK (Page 2)",
      description = output_string2
    )

    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)

    
    print("executed")
    
  # UPDATE IGN COMMAND - USES THE MASSIVE LIST AT THE TOP
  @commands.command(hidden=True)
  async def updateign(self,ctx, member: discord.Member = None):

    if(ctx.author.id != 332601516626280450): return

    global ign_list
    
    if(member):

      user = str(member.id)
      
      print("member present")

      if(user not in db):
        
        print("user not in db")

        db[user] = {
          "clan":{}
        }

        print("user added to db")

      # Loop through our global ignlist
      for entry in ign_list:

        if(user == entry["discid"]):
          
          print("user found in ign_list")
          start_date = entry["startdate"]
          ign = entry["name"]

          db[user]["clan"] = {
            "start" : start_date,
            "ign" : ign
          }

          await ctx.send("User found:\nIGN: " + ign + "\nStart date: " + start_date)
    else:
      
      # This will attempt to apply to all entries in the global ign_list
      for entry in ign_list:

        if(entry["discid"] == "empty"): continue
          
        user = str(entry["discid"])
        
        print(user)

        start_date = entry["startdate"]
        ign = entry["name"]

        if(user in db):
          db[user]["clan"] = {
            "start" : start_date,
            "ign" : ign
          }

        else:
          db[user] = {
            "clan" : {
            "start" : start_date,
            "ign" : ign
            }
          }
        print("member passthru completed")
        
      await ctx.send("Finished. Check .listdb")
    print("executed")
    
  # LIST MEMBERS COMMAND
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
    
    for entry in ign_list:
      
      datestart = entry["startdate"].replace("-", " ")
      
      d = datetime.strptime(datestart, '%d %b %Y')
      
      output_msg += entry["name"] + " - " + d.strftime('%d %b %Y') + " - " + entry["discid"] + "\n"


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
    
  # LIST DB COMMAND  
  @commands.command(hidden=True)
  async def listdb(self, ctx):

    if ctx.author.id != 332601516626280450: return
      
    embed = discord.Embed(title="All key-value entries in db - Page 1")
    embed2 = discord.Embed(title="All key-value entries in db - Page 2")
    embed3 = discord.Embed(title="All key-value entries in db - Page 3")

    i = 0
    for key, value in db.items():
      
      field_value = ""

      
      for a, b in value.items():

        
        field_value += f"{a} = {b}\n"
        
        
      person = ctx.bot.get_user(int(key))
      if(i > 48):
        embed3.add_field(
          name = person,
          value = field_value
        )
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
    await ctx.send(embed=embed3)

def setup(bot):
  bot.add_cog(Members(bot))