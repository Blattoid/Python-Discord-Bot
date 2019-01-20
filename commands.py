print("\tLoading command dependencies...")
#internal
print("\tInternal (1/2)")
from io import BytesIO #mca, beauty, protecc
from os import remove as delete_file #mca, beauty, protecc
from os import _exit as force_exit #shutdown
from random import randint #dice, coin_toss, rps, mca, beauty, protecc
import re #used to remove non-numbers from mentions to extract the user id
from requests import get #mca, beauty, protecc
from subprocess import PIPE as SUB_PIPE #exec
from subprocess import Popen as shell_exec #exec
from sys import version_info as python_info #help
from time import sleep #shutdown
#external (3rd party)
print("\tExternal (2/2)")
import pyfiglet #figlet
from PIL import Image #mca, beauty, protecc

def __getuserid__(string):
	re.sub("[^0-9]","",array[1])

from discord.ext import commands

#user commands
async def help(client):
	"""
	#get number of lines of code in this script and all scripts in the 'modules' folder.
	#this file
	with open("bot.py") as f:
		linecount = len(f.readlines())
	"""
	linecount = lengthofthisfile
	#everything in modules
	for scriptname in listdir("modules"):
		try:
			with open("modules\\"+scriptname) as f:
				linecount += len(f.readlines())
		except Exception:
			continue #ignore errors if a folder was selected
	#send help message to dm of user
	await client.send_message(message.author, """(User Commands)
```
These commands are accessible to all users.
Display this help.
"""+commandprefix+"""help
Tests if the bot is working.
"""+commandprefix+"""test
Rolls a dice with an optional minimum and maximum limits
"""+commandprefix+"""dice [minimum [maximum]
Gives advice on where to find oxygen. In other words, the perfect command.
"""+commandprefix+"""oxygen
Tosses a coin. That's it.
"""+commandprefix+"""coin_toss
Reverses the given text
"""+commandprefix+"""reverse <text>
Gets information about a mentioned user
"""+commandprefix+"""info <mention>
Gets the avatar of a mentioned user
"""+commandprefix+"""avatar <mention>
Play a game of rock paper scissors with the bot. (I promise it doesn't cheat)
"""+commandprefix+"""rps <rock/paper/scissors>
Gets the bot to repeat the input text. The bot will then try and delete your message to make it look real.
"""+commandprefix+"""say <text>
Gets the number of times the mentioned user has "meeped".
"""+commandprefix+"""list_meeps <mention>
This command allow translation to and from Basic Shadow, which is a language invented by <@284415695050244106>.
"""+commandprefix+"""translate <to/from> <english>
```

Image manipulation commands
```
"""+commandprefix+"""beauty <mention>
"""+commandprefix+"""protecc <mention>
```

Criminality Commands
```
These commands control or list the criminality values of a user.
"""+commandprefix+"""list_crime <mention>
"""+commandprefix+"""set_crime <mention> <value>
"""+commandprefix+"""change_crime <mention> <increment value by>
```

Trigger Words
```
These are words that have make the bot do something if you say them.

"meep"
"wheatley" AND "moron"
"pineapple"
"no u" or "no you"
"the more you know"
```

(Bot Administration Commands)
```
These commands are strictly for the bot owners. Accessing them will send a warning to the owner.

Shutdown the bot.
"""+commandprefix+"""shutdown
Retrieve stored value for user attribute in database
"""+commandprefix+"""getuserdata <mention> <attribute>
Update stored value for user attribute in database
"""+commandprefix+"""setuserdata <mention> <attribute> <value>
Execute a shell command on the host computer
"""+commandprefix+"""execute <shell command>
```
Created with `"""+str(linecount)+"""` lines of Python written by <@285465719292821506>.
Python version is """+str(python_info.major)+"."+str(python_info.minor)+".")
	await client.send_message(message.channel, "List of commands sent in DM.")
async def test(client):
	await client.send_message(message.channel, "Yes, <@"+message.author.id+">, This bot is online.")
async def dice(client):
	usage = "Usage: "+commandprefix+"dice [minimum] [maximum]"
	#get command parameters and allocate into appropriate variables.
	array = message_content.split()
	if len(array) > 1:
		try:
			min = int(array[1])
			max = int(array[2])
		except:
			error = format_exc()
			if "index" in error:
				#in the event that indexing fails (due to no or insufficient parameters, display the usage.
				await client.send_message(message.channel, usage)
			elif "invalid literal" in error:
				#in the event that conversion to an integer fails (likely due to text being entered instead of numbers), display this.
				await client.send_message(message.channel, """Minimum and maximum values must be numbers.
"""+usage)
			else:
				await client.send_message(message.channel, """Unknown error while reading array index.
`"""+error+"`")
				consoleOutput(error)
			return #end command
	else:
		#no parameters were specified, so the defaults are a regular die.
		min = 1
		max = 6

	if min<max:
		#roll the dice
		await client.send_message(message.channel, "I rolled "+str(randint(min,max)))
	else:
		await client.send_message(message.channel, "Minimum & maximum must be numbers.")
async def oxygen(client):
	await client.send_message(message.channel, "Look around and you will find it.")
async def coin_toss(client):
	result = randint(1,8)
	if result <= 4:
		result = "Tails"
	else:
		result = "Heads"
	await client.send_message(message.channel, result+".")
async def reverse(client):
	usage = "Usage: "+commandprefix+"reverse <text>"
	try:
		#remove command prefix from string we want
		text = message_content[len(commandprefix)+8:] #change according to length of command name + 1 for the space
	except:
		error = format_exc()
		await client.send_message(message.channel, """Error while reading text.
`"""+error+"`")
		consoleOutput(error)
		return #end command
	if not text.replace(" ","") == "":
		await client.send_message(message.channel, text[::-1]) #mystical string manipulation command to reverse the input
	else:
		await client.send_message(message.channel, usage)
async def info(client):
	usage = "Usage: "+commandprefix+"info <mention>"
	array = message_content.split()
	try:
		userid = __getuserid__(array[1])
	except:
		error = format_exc()
		if "IndexError" in error:
			await client.send_message(message.channel, usage)
		else:
			await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
			consoleOutput(error)
		return #end command

	try:
		user = await client.get_user_info(userid)
	except:
		error = format_exc()
		if "Unknown User" in error:
			await client.send_message(message.channel,"No user exists with the ID "+userid)
			consoleOutput("No user exists with the ID "+userid)
			return
	embed = discord.Embed(title="Data dump for user "+user.name+"#"+user.discriminator)
	embed.add_field(name="Is a bot", value=user.bot, inline=False)
	embed.add_field(name="Date created", value=user.created_at, inline=False)
	embed.add_field(name="Nickname", value=user.display_name, inline=False)
	embed.add_field(name="Unique ID", value=user.id, inline=False)
	embed.add_field(name="Avatar", value=".", inline=False)
	embed.set_image(url=user.avatar_url)
	await client.send_message(message.channel,embed=embed)
async def avatar(client):
	usage = "Usage: "+commandprefix+"avatar <mention>"
	array = message_content.split()
	try:
		userid = re.sub("[^0-9]","",array[1])
	except:
		error = format_exc()
		if "IndexError" in error:
			await client.send_message(message.channel, usage)
		else:
			await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
			consoleOutput(error)
		return #end command

	try:
		user = await client.get_user_info(userid)
		embed = discord.Embed(title="Avatar for user "+user.name+"#"+user.discriminator)
		embed.set_image(url=user.avatar_url)
		await client.send_message(message.channel,embed=embed)
	except:
		error = format_exc()
		if "Unknown User" in error:
			await client.send_message(message.channel,"No user exists with the ID "+userid)
			consoleOutput("No user exists with the ID "+userid)
		else:
			await client.send_message(message.channel,"""Unknown error!
`"""+error+"`")
			consoleOutput("""Unknown error!
"""+error)
		return
async def rps(client):
	usage = "Usage: "+commandprefix+"rps <rock/paper/scissors>"
	array = message_content.split()
	try:
		userchoice = array[1].lower()
	except:
		error = format_exc()
		if "IndexError" in error:
			await client.send_message(message.channel, usage)
			
		else:
			await client.send_message(message.channel, """Error while reading parameter.
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
		await client.send_message(message.channel, "You chose "+userchoice+". I chose "+cpuchoice+". Tie!")
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
		await client.send_message(message.channel, """Invalid option.
"""+usage)
		return

	#send result
	await client.send_message(message.channel, "You chose "+userchoice+". I chose "+cpuchoice+". "+result)
async def say(client):
	usage = "Usage: "+commandprefix+"say <text>"
	try:
		#remove command prefix from string we want
		text = message.content[len(commandprefix)+4:] #change according to length of command name + 1 for the space
	except:
		error = format_exc()
		await client.send_message(message.channel, """Error while reading text.
`"""+error+"`")
		consoleOutput(error)
		return #end command
	if not text.replace(" ","") == "":
		await client.send_message(message.channel, text) #send the message that the user wanted
		await client.delete_message(message) #cover their tracks for them
	else:
		await client.send_message(message.channel, usage)
async def list_meeps(client):
	usage = "Usage: "+commandprefix+"list_meeps <mention>"
	array = message_content.split()
	try:
		userid = re.sub("[^0-9]","",array[1])
	except:
		error = format_exc()
		if "IndexError" in error:
			await client.send_message(message.channel, usage)
		else:
			await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
			consoleOutput(error)
		return #end command
	value = str(userData.get_user_data(userid,"meeps"))
	await client.send_message(message.channel, "<@"+userid+"> has meeped "+value+" times.")
async def mca(client):
	usage = "Usage: "+commandprefix+"mca <text>"
	try:
		#remove command prefix from string we want
		text = message_content[len(commandprefix)+4:] #change according to length of command name + 1 for the space
	except:
		error = format_exc()
		await client.send_message(message.channel, """Error while reading text.
`"""+error+"`")
		consoleOutput(error)
		return #end command
	if not text.replace(" ","") == "":
		iconid = randint(1,39)
		response = get('https://www.minecraftskinstealer.com/achievement/a.php?i=%s&h=%s&t=%s' % (iconid, "Achievement get!", text))
		img = Image.open(BytesIO(response.content))

		#unfortunately you cannot send a pillow object using discord.py directly. it must be loaded from a file.
		imageid = str(randint(1,99999999))+".png"  #just to make sure nothing is overwritten in heavy loads.
		img.save(imageid) #save it...
		await client.send_file(message.channel, imageid) #then send the image.
		delete_file(imageid) #delete the file afterwards.
	else:
		await client.send_message(message.channel, usage)
async def translate(client):
	usage = "Usage: "+commandprefix+"translate <to/from> <text>"
	#get command parameters and allocate into appropriate variables.
	array = message_content.split()
	try:
		mode = array[1].lower()
	except:
		error = format_exc()
		if "index" in error:
			#in the event that indexing fails (due to no or insufficient parameters), display the usage.
			await client.send_message(message.channel, """Missing parameter.
"""+usage)
		else:
			await client.send_message(message.channel, """Unknown error while reading array index.
`"""+error+"`")
			consoleOutput(error)
			return #end command

		if "to" not in message_content.lower() and "from" not in message_content.lower(): #check for invalid mode
			await client.send_message(message.channel, """Invalid mode.
"""+usage)
			return #end command
		#proper mode selected, lets get separate the text to be translated from the command
		length = len("translate")+2+len(mode) #length of command, 2 for the space, then the length of the mode
		text = message_content[length::].upper() #separate it then capitalize
		if mode == "from":
			await client.send_message(message.channel, "`"+shadowtranslator.ConvertFromShadow(text)+"`")
		elif mode == "to":
			await client.send_message(message.channel, "`"+shadowtranslator.ConvertToShadow(text)+"`")
		else:
			#wat.
			#how did you get here??
			raise ExcuseMeWhatTheFuckError("Unexpected error in mode selection")
async def figlet(client):
	usage = "Usage: "+commandprefix+"figlet <text>"
				
	#find length of input text, then isolate it from the command.
	length = len("figlet")+2 #length of command then 2 for the space
	text = message_content[length::].upper().replace(" ","\n") #separate it then capitalize, then replace spaces with newlines
				
	#check if the input text is empty. if it is, show the usage.
	if text.split() == []:
		await client.send_message(message.channel, usage)
		return
				
	try:
		await client.send_message(message.channel, "```"+pyfiglet.figlet_format(text)+"```")
	except discord.errors.HTTPException:
		await client.send_message(message.channel, "Message too long.")
				
#image manipulation commands
async def beauty(client):
	usage = "Usage: "+commandprefix+"beauty <mention>"
	array = message_content.split()
	try:
			userid = re.sub("[^0-9]","",array[1])
	except:
			error = format_exc()
			if "IndexError" in error:
				await client.send_message(message.channel, usage)
				return #end command
			else:
				await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
				consoleOutput(error)
				return
	background = Image.open("images\\beauty.jpg").convert("RGBA") #original meme image

	userdata = await client.get_user_info(userid) #retrieve information of user
	response = get(userdata.avatar_url) #get the image data from the avatar_url and store that into response.
	foreground = Image.open(BytesIO(response.content)).convert("RGBA") #parse response into Image object. This contains the pfp.

	foreground = foreground.resize((150,175)) #make foreground the correct size for the target area
	background.paste(foreground, (437, 38), foreground) #move the foreground into the correct area for the first target area
	background.paste(foreground, (440, 380), foreground) #move the foreground into the correct area for the second target area

	#unfortunately you cannot send a pillow object using discord.py directly. it must be loaded from a file.
	imageid = str(randint(1,99999999))+".png"  #just to make sure nothing is overwritten in heavy loads.
	background.save(imageid) #save it...
	await client.send_file(message.channel, imageid) #then send the image.
	delete_file(imageid) #delete the file afterwards.
async def protecc(client):
				usage = "Usage: "+commandprefix+"protecc <mention>"
				array = message_content.split()
				try:
						userid = re.sub("[^0-9]","",array[1])
				except:
						error = format_exc()
						if "IndexError" in error:
								await client.send_message(message.channel, usage)
								return #end command
						else:
								await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
								consoleOutput(error)
								return
				background = Image.open("images\\protecc.png").convert("RGBA") #original meme image

				userdata = await client.get_user_info(userid) #retrieve information of user
				response = get(userdata.avatar_url) #get the image data from the avatar_url and store that into response.
				foreground = Image.open(BytesIO(response.content)).convert("RGBA") #parse response into Image object. This contains the pfp.

				foreground = foreground.resize((124,170)).rotate(-24, expand=1) #rotate foreground and make the correct size for the target area
				background.paste(foreground, (391, 131), foreground) #move the foreground into the correct area for the target area

				#unfortunately you cannot send a pillow object using discord.py directly. it must be loaded from a file.
				imageid = str(randint(1,99999999))+".png"  #just to make sure nothing is overwritten in heavy loads.
				background.save(imageid) #save it...
				await client.send_file(message.channel, imageid) #then send the image.
				delete_file(imageid) #delete the file afterwards.

#criminality commands
async def list_crime(client):
				usage = "Usage: "+commandprefix+"list_crime <mention>"
				array = message_content.split()
				try:
						userid = re.sub("[^0-9]","",array[1])
				except:
						error = format_exc()
						if "IndexError" in error:
								await client.send_message(message.channel, usage)
								return #end command
						else:
								await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
								consoleOutput(error)
								return

				if len(array) != 2:
						await client.send_message(message.channel, usage)
						return
				value = userData.get_user_data(userid,"criminality")
				await client.send_message(message.channel, "Criminality value for <@"+userid+"> is "+str(value)+".")
				consoleOutput("Criminality value is now "+str(value)+".")
async def set_crime(client):
				usage = "Usage: "+commandprefix+"set_crime <mention> <value>"
				array = message_content.split()
				try:
						userid = re.sub("[^0-9]","",array[1])
				except:
						error = format_exc()
						if "IndexError" in error:
								await client.send_message(message.channel, usage)
								return #end command
						else:
								await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
								consoleOutput(error)
								return
				if len(array) != 3:
						await client.send_message(message.channel, usage)
						return
				value = array[2]
				userData.set_user_data(userid,"criminality",value)
				await client.send_message(message.channel, "Updated criminality value for <@"+userid+"> to "+str(value)+".")
				consoleOutput("Updated value to "+str(value)+".")
async def change_crime(client):
				usage = "Usage: "+commandprefix+"change_crime <mention> <value>"
				array = message_content.split()
				try:
						userid = re.sub("[^0-9]","",array[1])
				except:
						error = format_exc()
						if "IndexError" in error:
								await client.send_message(message.channel, usage)
								return #end command
						else:
								await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
								consoleOutput(error)
								return

				if len(array) != 3:
						await client.send_message(message.channel, usage)
						return

				prevvalue = userData.get_user_data(userid,"criminality")
				value = array[2]
				if (type(prevvalue)) == str:
						prevvalue = 0
				if (type(value)) == str:
						value = 0
				finalvalue = prevvalue+value
				userData.set_user_data(userid,"criminality",finalvalue)

				await client.send_message(message.channel, "Changed criminality value for <@"+userid+"> by "+str(value)+" to equal "+str(finalvalue)+".")
				consoleOutput("Changed criminality value by "+str(value)+" to equal "+str(finalvalue)+".")

#exclusive management commands. foolproofing isnt required since only i can use them
async def shutdown(client):
				#id check
				if isAdmin(message.author.id):
						await client.send_message(message.channel, "Access granted. Shutting down bot.")
						consoleOutput("Access granted. Shutting down bot.")
						await client.change_presence(status=discord.Status.invisible)
						sleep(2)
						force_exit(0)
				else:
						await reportAccessDenied(message)
						consoleOutput("Access denied.")
async def getuserdata(client):
				#id check
				if isAdmin(message.author.id):
						array = message_content.split()
						userid = re.sub("[^0-9]","",array[1])
						await client.send_message(message.channel, "Access granted.")
						consoleOutput("Access granted.")
						value = str(userData.get_user_data(userid,array[2]))
						await client.send_message(message.channel, "Value stored with name '"+array[2]+"' for <@"+userid+"> is "+value)
						consoleOutput("Value stored is "+value)
				else:
						await reportAccessDenied(message)
						consoleOutput("Access denied.")
async def setuserdata(client):
				#id check
				if isAdmin(message.author.id):
						array = message_content.split()
						userid = re.sub("[^0-9]","",array[1])
						await client.send_message(message.channel, "Access granted. Setting user data for <@"+userid+">.")
						consoleOutput("Access granted. Setting user data.")
						userData.set_user_data(userid,array[2],array[3])
						await client.send_message(message.channel, "Updated value.")
						consoleOutput("Updated value.")
				else:
						await reportAccessDenied(message)
						consoleOutput("Access denied.")
async def execute(client):
	#id check
	if isAdmin(message.author.id):
			await client.send_message(message.channel, "Access granted. Executing command...")
			consoleOutput("Access granted. Executing command...")
			cmd = message_content[len(commandprefix)+5:]
			output = str(bytes(str(shell_exec(cmd, shell=True, stdout=SUB_PIPE).stdout.read()), "utf-8").decode("unicode_escape"))
			#trim "b' " and "'" from start and end.
			output = output[3:]
			output = output[:-1]
			#send it :D
			await client.send_message(message.channel, """```
"""+output+"```")
	else:
		await reportAccessDenied(message)
		consoleOutput("Access denied.")