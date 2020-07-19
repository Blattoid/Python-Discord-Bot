from commands.modules.common import *
from traceback import format_exc #for error handling

#internal
from random import randint #dice, coin_toss, rps
from requests import get as get_request #mca, scp_read
from sys import version_info as python_info #help
from io import BytesIO #mca

#external
import discord #avatar, info, mca
import pyfiglet #figlet
import wikipedia as wiki #wikipedia
from html2text import html2text #scp_read
from PIL import Image #mca
from commands.modules import shadow_translator #translate (i made this one :D)
shadowtranslator = shadow_translator.ShadowTranslator()

def split_into_snippets(text, desired_snippet_length=1980, delimiter=" "):
	"""Given a long string, split it up into snippets of a specified length. Useful for formatting a long message into several sendable messages."""
	snippets = []
	i = 0
	offset = 0
	last_known_space = 0
	while i < len(text): #loop over the text
		if text[i] == delimiter: last_known_space = i #scan for spaces.
		if i-offset >= desired_snippet_length: #if we exceed the desired length...
			#print everything behind that space to where we last printed.
			snippets.append(text[offset:][:last_known_space-offset])
			offset = last_known_space + 1 #begin a new snippet.
		i += 1 #increment our 'cursor'
	snippets.append(text[offset:][:len(text)]) #the last snippet should have any leftover text.
	return snippets

#general commands
async def help(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	#send help message to dm of user
	await message.author.send("""General Commands
```
These commands do not have a classification.
Display this help.
{0}help
Tests if the bot is working.
{0}test
Rolls a dice with an optional minimum and maximum limits.
{0}dice [minimum] [maximum]
Gives advice on where to find oxygen. In other words, the perfect command.
{0}oxygen
Tosses a coin. That's it.
{0}coin_toss
Reverses the given text.
{0}reverse <text>
Gets information about a mentioned user.
{0}info <mention>
Gets the avatar of a mentioned user.
{0}avatar <mention>
Play a game of rock paper scissors with the bot. (I promise it doesn't cheat)
{0}rps <rock/paper/scissors>
Gets the bot to repeat the input text. The bot will then try and delete your message to make it look real.
{0}say <text>
Gets the number of times the mentioned user has "meeped".
{0}list_meeps <mention>
Generates a Minecraft achievement with a random icon, with text based on the input.
{0}mca <text>
This command allow translation to and from Basic Shadow, which is a language invented by <@284415695050244106{0}.
{0}translate <to/from> <input>
Generates an ASCII art of the input text.
{0}figlet <text>
Gets a Wikipedia page on a topic. If the topic name includes spaces, wrap it in quotation marks.
{0}wikipedia <topic>
Retrieves an SCP document for any SCP.
{0}scp <scp id>
```""".format(commandprefix))
	await message.author.send("""
Image manipulation commands
```
{0}beauty <mention>
{0}protecc <mention>
{0}deepfry
```

Voice channel commands
```
Rickrolls the voice channel you are connected to.
{0}rickroll
Plays a youtube video either from a URL or from a search term. This is not entirely stable and can occasionally crash. I blame FFMPEG.
{0}play <url/search term>
Runs the input text through text to speech and speaks it.
{0}s <text>
Disconnects the bot from the current voice channel.
{0}disconnect
```

Currency Commands
```
These commands are for the builtin currency system that can be used in servers.
{0}balance [mention]

These money commands can only be run by a Bot Admin.
{0}add_money <mention> <value>
{0}set_money <mention> <value>
{0}globalset_money <mention> <value>
```

Trigger Words
```
These are words that have make the bot do something if you say them.
	"meep"
	"wheatley" AND "moron"
	"the more you know"
```

Bot Administration Commands
```
These commands can only be run by the Bot Admins.
Shutdown the bot.
{0}shutdown
Attempts to update the bot's nickname on a server. Leave empty to reset to nothing.
{0}nickname <new name>
Execute a shell command on the host computer.
{0}execute <shell command>
Deletes a certain number of messages in the same channel that the command was sent.
{0}purge <number of messages>
```
Created by <@285465719292821506>.
Python version is {1}.{2}""".format(commandprefix,str(python_info.major),str(python_info.minor)))
	await message.channel.send("List of commands sent in DM.")

async def test(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	await message.channel.send("Yes, <@"+str(message.author.id)+">. This bot is online.")

async def dice(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]

	usage = "Usage: "+commandprefix+"dice [minimum] [maximum]"
	#get command parameters and allocate into appropriate variables.
	array = message.content.split()
	if len(array) > 1:
		try:
			min = int(array[1])
			max = int(array[2])
		except:
			error = format_exc()
			if "index" in error:
				#in the event that indexing fails (due to no or insufficient parameters, display the usage.
				await message.channel.send(usage)
			elif "invalid literal" in error:
				#in the event that conversion to an integer fails (likely due to text being entered instead of numbers), display this.
				await message.channel.send("""Minimum and maximum values must be numbers.
"""+usage)
			else:
				await message.channel.send("""Unknown error while reading array index.
`"""+error+"`")
				consoleOutput(error)
			return #end command
	else:
		#no parameters were specified, so the defaults are a regular die.
		min = 1
		max = 6

	if min<max:
		#roll the dice
		await message.channel.send("I rolled "+str(randint(min,max)))
	else:
		await message.channel.send("Minimum & maximum must be numbers.")

async def oxygen(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	await message.channel.send("Look around and you will find it.")

async def coin_toss(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	result = randint(1,8)
	if result <= 4:
		result = "Tails"
	else:
		result = "Heads"
	await message.channel.send(result+".")

async def reverse(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]

	usage = "Usage: "+commandprefix+"reverse <text>"
	try:
		#remove command prefix from string we want
		text = message.content[len(commandprefix)+8:] #change according to length of command name + 1 for the space
	except:
		error = format_exc()
		await message.channel.send("""Error while reading text.
`"""+error+"`")
		consoleOutput(error)
		return #end command
	if not text.replace(" ","") == "":
		await message.channel.send(text[::-1]) #mystical string manipulation command to reverse the input
	else:
		await message.channel.send(usage)

async def info(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	client = passedvariables["client"]

	usage = "Usage: "+commandprefix+"info <mention>"
	array = message.content.split()
	try:
		userid = getUserId(array[1])
	except:
		error = format_exc()
		if "IndexError" in error:
			await message.channel.send(usage)
		else:
			await message.channel.send("""Error while formatting mention into user id.
`"""+error+"`")
			consoleOutput(error)
		return #end command

	try:
		user = await client.fetch_user(userid)
	except:
		error = format_exc()
		if "NotFound" in error:
			await message.channel.send("No user exists with the ID "+userid)
			consoleOutput("No user exists with the ID "+userid)
		else:
			await message.channel.send("""Unknown error!
`"""+error+"`")
			consoleOutput("""Unknown error!
"""+error)
		return
	embed = discord.Embed(title="Data dump for user "+user.name+"#"+user.discriminator)
	embed.add_field(name="Is a bot", value=user.bot, inline=False)
	embed.add_field(name="Date created", value=user.created_at, inline=False)
	embed.add_field(name="Nickname", value=user.display_name, inline=False)
	embed.add_field(name="Unique ID", value=user.id, inline=False)
	embed.add_field(name="Avatar", value=".", inline=False)
	embed.set_image(url=user.avatar_url)
	await message.channel.send(embed=embed)

async def avatar(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	client = passedvariables["client"]

	usage = "Usage: "+commandprefix+"avatar <mention>"
	array = message.content.split()
	try:
		userid = getUserId(array[1])
	except:
		error = format_exc()
		if "IndexError" in error:
			await message.channel.send(usage)
		else:
			await message.channel.send("""Error while formatting mention into user id.
`"""+error+"`")
			consoleOutput(error)
		return #end command

	try:
		user = await client.fetch_user(userid)
	except:
		error = format_exc()
		if "NotFound" in error:
			await message.channel.send("No user exists with the ID "+userid)
			consoleOutput("No user exists with the ID "+userid)
		else:
			await message.channel.send("""Unknown error!
`"""+error+"`")
			consoleOutput("""Unknown error!
"""+error)
		return
	embed = discord.Embed(title="Avatar for user "+user.name+"#"+user.discriminator)
	embed.set_image(url=user.avatar_url)
	await message.channel.send(embed=embed)

async def rps(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]

	usage = "Usage: "+commandprefix+"rps <rock/paper/scissors>"
	array = message.content.split()
	try:
		userchoice = array[1].lower()
	except:
		error = format_exc()
		if "IndexError" in error:
			await message.channel.send(usage)

		else:
			await message.channel.send("""Error while reading parameter.
`"""+error+"`")
			consoleOutput(error)
		return #end command

	#cpu choice logic
	cpuchoice = randint(1,3)
	if cpuchoice == 1:
		cpuchoice = "rock"
	elif cpuchoice == 2:
		cpuchoice = "paper"
	else:
		cpuchoice = "scissors"

	#game logic
	#tie
	if cpuchoice == userchoice:
		await message.channel.send("You chose "+userchoice+". I chose "+cpuchoice+". Tie!")
		return

	#user wins
	if userchoice == "rock" and cpuchoice == "scissors": result="You won!"
	elif userchoice == "paper" and cpuchoice == "rock": result="You won!"
	elif userchoice == "scissors" and cpuchoice == "paper": result="You won!"

	#cpu wins
	elif cpuchoice == "rock" and userchoice == "scissors": result="You lost!"
	elif cpuchoice == "paper" and userchoice == "rock": result="You lost!"
	elif cpuchoice == "scissors" and userchoice == "paper": result="You lost!"

	#edge case. triggered if user entered invalid string.
	else:
		await message.channel.send("""Invalid option.
"""+usage)
		return

	#send result
	await message.channel.send("You chose "+userchoice+". I chose "+cpuchoice+". "+result)

async def say(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]

	usage = "Usage: "+commandprefix+"say <text>"
	try:
		#remove command prefix from string we want
		text = message.content[len(commandprefix)+4:] #change according to length of command name + 1 for the space
	except:
		error = format_exc()
		await message.channel.send("""Error while reading text.
`"""+error+"`")
		consoleOutput(error)
		return #end command
	if not text.replace(" ","") == "":
		await message.channel.send(text) #send the message that the user wanted
		try:
			await message.delete() #cover their tracks for them
		except:
			pass #ignore errors that arise from insufficient permissions
	else:
		await message.channel.send(usage)

async def list_meeps(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	userData = passedvariables["userData"]

	usage = "Usage: "+commandprefix+"list_meeps <mention>"
	array = message.content.split()
	try:
		userid = getUserId(array[1])
	except:
		error = format_exc()
		if "IndexError" in error:
			await message.channel.send(usage)
		else:
			await message.channel.send("""Error while formatting mention into user id.
`"""+error+"`")
			consoleOutput(error)
		return #end command
	value = str(userData.get_user_data(userid,"meeps"))
	await message.channel.send("<@"+userid+"> has meeped "+value+" times.")

async def mca(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]

	usage = "Usage: "+commandprefix+"mca <text>"
	try:
		#remove command prefix from string we want
		text = message.content[len(commandprefix)+4:] #change according to length of command name + 1 for the space
	except:
		error = format_exc()
		await message.channel.send("""Error while reading text.
`"""+error+"`")
		consoleOutput(error)
		return #end command
	if not text.replace(" ","") == "":
		iconid = randint(1,39)
		response = get_request('https://www.minecraftskinstealer.com/achievement/a.php?i=%s&h=%s&t=%s' % (iconid, "Achievement get!", text))
		img = Image.open(BytesIO(response.content))

		#unfortunately you cannot send a pillow object using discord.py directly. it must be loaded from a file.
		imageid = str(randint(1,99999999))+".png"  #just to make sure nothing is overwritten in heavy loads.
		img.save(imageid) #save it...
		await message.channel.send(file=discord.File(imageid, filename="img.png")) #then send the image.
		delete_file(imageid) #delete the file afterwards.
	else:
		await message.channel.send(usage)

async def translate(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]

	usage = "Usage: "+commandprefix+"translate <to/from> <text>"
	#get command parameters and allocate into appropriate variables.
	array = message.content.split()
	try:
		mode = array[1].lower()
	except:
		error = format_exc()
		if "index" in error:
			#in the event that indexing fails (due to no or insufficient parameters), display the usage.
			await message.channel.send("""Missing parameter.
"""+usage)
		else:
			await message.channel.send("""Unknown error while reading array index.
`"""+error+"`")
			consoleOutput(error)
			return #end command

	if "to" not in message.content.lower() and "from" not in message.content.lower(): #check for invalid mode
		await message.channel.send("""Invalid mode.
"""+usage)
		return #end command
	#proper mode selected, lets get separate the text to be translated from the command
	length = len(commandprefix+"translate")+1+len(mode) #length of command, 2 for the space, then the length of the mode
	text = message.content[length::].upper() #separate it then capitalize
	if mode == "from":
		await message.channel.send("`"+shadowtranslator.ConvertFromShadow(text)+"`")
	elif mode == "to":
		await message.channel.send("`"+shadowtranslator.ConvertToShadow(text)+"`")
	else:
		#wat.
		#how did you get here??
		raise ExcuseMeWhatTheFuckError("Unexpected error in mode selection")

async def figlet(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]

	usage = "Usage: "+commandprefix+"figlet <text>"

	#find length of input text, then isolate it from the command.
	length = len(commandprefix+"figlet")+1 #length of command then 1 for the space
	text = message.content[length::].replace(" ","\n") #separate it then replace spaces with newlines

	#check if the input text is empty. if it is, show the usage.
	if text.split() == []:
		await message.channel.send(usage)
		return

	try:
		await message.channel.send("```"+pyfiglet.figlet_format(text)+"```")
	except discord.errors.HTTPException:
		await message.channel.send("Message too long.")

async def wikipedia(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]

	usage = "Usage: "+commandprefix+"wikipedia <topic>"

	#find length of input text, then isolate it from the command.
	length = len(commandprefix+"wikipedia")+1 #length of command then 1 for the space
	searchterm = message.content[length::] #separate search term from command

	#check if the input text is empty. if it is, show the usage.
	if searchterm.split() == []:
		await message.channel.send(usage)
		return

	try:
		page = wiki.page(searchterm) #get the wikipedia page for that topic
		summary = page.summary[:1990] #get the first 2000 or so characters. this max limit is imposed by Discord message length limits.
		await message.channel.send("```"+summary+"```") #send the summary
	except wiki.requests.exceptions.ConnectionError:
		await message.channel.send("Unable to connect to Wikipedia.")
	except wiki.exceptions.PageError:
		await message.channel.send("Wikipedia page does not exist.")
	except wiki.exceptions.DisambiguationError:
		error = format_exc() #get the traceback
		removeterm = "DisambiguationError: "
		error = error[error.find(removeterm)+len(removeterm):] #remove everything up to the end of the substring "DisambiguationError"
		await message.channel.send(error) #return what is left

async def scp_read(passedvariables):
		#include all the required variables
		message = passedvariables["message"]
		commandprefix = passedvariables["commandprefix"]

		usage = "Usage: "+commandprefix+"scp <scp id>"
		array = message.content.split()
		try:
			scp_id = int(array[1]) #get the scp document id
		except:
			error = format_exc()
			if "ValueError" in error or "IndexError" in error:
				await message.channel.send(usage)
			else:
				await message.channel.send("""Unknown error while parsing arguments.
	`"""+error+"`")
				consoleOutput(error)
			return #end command

		#simple check to ensure the id is not smaller than 0.
		if scp_id < 0:
			await message.channel.send("Id is smaller than 0.")
			return

		#another check to make sure that the id fits the format.
		#example: scp_id 55 should be 055
		scp_id = str(scp_id)
		while len(scp_id) < 3: scp_id = "0"+scp_id

		await message.channel.send("Accessing restricted document SCP-{0}...".format(scp_id)) #notification that the request of the document was understood.

		#download the page and get the html from the request.
		url = 'http://www.scp-wiki.net/scp-'+str(scp_id)
		try:
			response = get_request(url).text
		except Exception as err:
			await message.channel.send("Internal error while loading document: "+err)
			return
		text = html2text(response) #extract all the text from the html with minimal formatting
		if len(text) < 5: #check to ensure the server actually returned something.
			await message.channel.send("Internal error loading document: No HTML was returned. Status code is "+str(response.status_code))
			return

		await message.channel.send("Received {0} bytes of data. Decrypting...".format(len(text))) # notification that the download suceeded.
		#this isn't actually decryption, of course. it just says that to make it seem like you are accessing something you shouldn't, to align with the canon of the universe.
		text_copy = text #just in case we cant extract the document, we will need to revert afterwards.
		text = text[text.find("**Item #:**"):]#strip everything behind the SCP ID
		text = text[:text.rfind("« ")] #strip everything past this designated end string, which is where the document ends.

		#occasionally, the previous code fails to detect the document due to the non-consistent nature of the documents.
		#this second attempt triggers if that has happened.
		if len(text) < 5:
			await message.channel.send("Standard decryption method failed. Retrying with alternate method.")
			text = text_copy
			text = text[text.find("SCP-"+str(scp_id)):]#strip everything behind the SCP ID
			text = text[:text.rfind("« ")] #strip everything past this designated end string, which is where the document ends.
			if len(text) < 5: #if it still didn't work, just give them a link to the article. we tried our best.
				await message.channel.send("Alternate decryption method failed. Apologies. "+url)
				return #end the command here.

		#Split the text up into 'snippets', each a maximum of 1980 characters. A snippet should never cut through a word halfway.
		snippets = split_into_snippets(text)

		#finally, send all of the snippets back.
		for snippet in snippets: await message.channel.send("```"+snippet+" ```")
		await message.channel.send("[DOCUMENT END]")
