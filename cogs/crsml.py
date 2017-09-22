"""
The MIT License (MIT)
Copyright (c) 2017 Dino
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __main__ import send_cmd_help
import requests
import os
import time
import discord
from discord.ext import commands
import json
from bs4 import BeautifulSoup
import urllib
import urllib.request 
import asyncio
import aiohttp
from .utils.dataIO import dataIO
from cogs.utils import checks
import locale
racfclans = {
	"ALPHA" : "2CCCP",
	"BRAVO" : "2U2GGQJ",
	"CHARLIE" : "2QUVVVP",
	"DELTA" : "Y8GYCGV",
	"ECHO" : "LGVV2CG",
	"ESPORTS" : "R8PPJQG",
	"FOXTROT" : "QUYCYV8",
	"GOLF" : "GUYGVJY",
	"HOTEL" : "UGQ28YU",
	"MINI" : "22LR8JJ2",
	"MINI2" : "2Q09VJC8"
}
racfclanslist = [
	"Alpha",
	"Bravo",
	"Charlie",
	"Delta",
	"Echo",
	"eSports",
	"Foxtrot",
	"Golf",
	"Hotel",
	"Mini",
	"Mini2"
]
BOTCMDER = ["Bot Commander"]
NUMITEMS = 9
statscr_url = "http://statsroyale.com/profile/"
crapiurl = 'http://api.cr-api.com'
crapi_url = 'http://cr-api.com'
statsurl = 'http://statsroyale.com'
PATH = os.path.join("data", "crtags")
SETTINGS_JSON = os.path.join(PATH, "settings.json")
BACKSETTINGS_JSON = os.path.join(PATH, "backsettings.json")
CLAN_JSON = os.path.join(PATH, "clan.json")
CREMOJIS_JSON = os.path.join(PATH, "cremojis.json")
SET_JSON = os.path.join(PATH, "set.json")
cremojis = dataIO.load_json(CREMOJIS_JSON)
validChars = ['0', '2', '8', '9', 'C', 'G', 'J', 'L', 'P', 'Q', 'R', 'U', 'V', 'Y']
tags = {}
headers = {
	'User-Agent': 'Bot(Rain), (https://github.com/Dino0631/discordbot/tree/master)',
	'From': 'htmldino@gmail.com'  
}
def api2emoji(cardname):
	return cardname.replace('_','')

async def async_refresh(url):
	async with aiohttp.get(url) as r:
		# response = await r.json()
		a = 1
		
class CRClan:

	def __init__(self):
		self.a = 1

	@classmethod
	async def create(self, tag):
		tag2id = dataIO.load_json(BACKSETTINGS_JSON)
		self.member_count = 0                           #done
		self.members = []                               #done
		self.clan_tag = tag                             #done
		self._url = crapiurl + '/clan/' + tag       	#done
		self.url = crapi_url + '/clan/' + tag 			#done
		self.tr_req = '0'                               #done
		self.clan_trophy = ''                           #done
		self.name = ''                                  #done
		self.donperweek = ''							#done
		self.desc = ''									#done
		self.badge = ''									#done
		self.leader = {}								#done
		self.size = 0									#done
		self.coleaders = []								#done
		self.elders = []								#done
		self.norole = []								#done
		# if clan_url != '':
		async with aiohttp.ClientSession() as session:
			async with session.get(self._url) as resp:
				datadict = await resp.json()
		
		# for x in datadict:
		# 	try:
		# 		print(x)
		# 	except:
		# 		print('some key')
		# 	try:
		# 		print(datadict[x])
		# 	except:
		# 		print('some value')
		# for member in datadict['members']:
		# 	try:
		# 		print(member)
		# 	except:
		# 		print('some member')
		# r = requests.get(self.clan_url, headers=headers)
		# html_doc = r.text

		for i, m in enumerate(datadict['members']):
			rank = str(m['currentRank'])
			name = str(m['name'])
			tag = str(m['tag']).upper()
			url = crapiurl +'/profile/'+ tag
			level = str(m['expLevel'])
			trophy = str(m['score'])
			donations = str(m['donations'])
			role = str(m['roleName'])
			if tag in tag2id:
				userid = tag2id[tag]
			else:
				userid = ''
			memberdict = {
				'name' : name.strip(),
				'rank' : rank.strip(),
				'tag' : tag.strip(),
				'userid': userid.strip(),
				'url' : url.strip(),
				'level' : level.strip(),
				'trophy' : trophy.strip(),
				'donations' : donations.strip(),
				'role' : role.strip()
			}
			memberdict['formatted'] = '`'+ memberdict['role']+'` ' + memberdict['name']+' [`#'+memberdict['tag']+'`]('+memberdict['url'].replace('api.', '', 1)+')'
			if memberdict['userid'] != '':
				try:
					memberdict['formatted'] += ' <@'+memberdict['userid'] + '>'
				except:
					pass
			if memberdict['role'] == 'Co-Leader':
				self.coleaders.append(memberdict)
			if memberdict['role'] == 'Member':
				self.norole.append(memberdict)
			if memberdict['role'] == 'Elder':
				self.elders.append(memberdict)
			if memberdict['role'] == 'Leader':
				self.leader = memberdict
			self.size += 1
			self.members.append(memberdict)

		self.clan_badge = crapiurl + datadict['badge_url']
		self.name = datadict['name']
		self.desc = datadict['description']
		d = self.desc
		
		d2 = d

		i = 0
		index = 0
		count = d2.lower().count('discord.')
		while i<count:
			index = d2.lower().find('discord.', index+1)
			d4 = d2.replace(d2[index:index+len('discord.')], 'discord.')
			d3 = d4[index:]
			endlink = d3[d3.find('discord.'):].find(' ')
			if endlink == -1:
				endlink = len(d3)
			discordlink = d3[d3.find('discord.'):endlink+d3.find('discord.')]
			d2 = d2.replace(d2[index:index+len(discordlink)], " [{}](https://{})".format(d2[index:index+len(discordlink)], discordlink))

			i += 1
		sym = '#'
		numtagsind2 = 0
		tagsind2 = []
		index = 0
		i = 0
		while i<d2.count(sym):
			index = d2.find(sym, index+1)
			x = ''
			i2 = 1
			thing = ''
			while x != ' ':
				thing += x
				x = d2[index+i2]
				i2 += 1
			valid = True
			n = 0
			thing2 = ''
			for l in thing:
				if l not in validChars:
					if n>4 and not l.isalnum():
						valid = True
					else:
						valid = False
					break
				thing2 += l
				n+=1
			if valid and len(thing2)>4:
				numtagsind2 += 1
				tagsind2.append(thing2)
			i += 1
		for tag in tagsind2:
			tag = tag.replace(sym, '')
			d2 = d2.replace(sym+tag, '[{}]({})'.format(sym+tag, 'https://cr-api.com/clan/'+tag))
		self.desc2 =  d2
		self.clan_trophy = datadict['score']
		self.tr_req = datadict['requiredScore']
		self.donperweek = datadict['donations']
		return self

class XP:
	def __init__(self, denom, xp, level):
		self.current = xp
		self.denom = denom
		self.level = level
	
	@property
	def xpleft(self):
		return self.denom-self.current
	@property
	def formatted(self):
		return "Level {}, {}/{}{}".format(self.level, self.current,self.denom, cremojis['experience'])

class Arena:
	def __init__(self, imageurl,name):
		self.url = imageurl
		self.name = name
	@property
	def formatted(self):
		return "Arena: {}".format(self.name)
class Card:
	def __init__(self, name, rarity, level, count, denom):
		self.name = name
		self.rarity = rarity
		self.level = level
		self.count = count
		self.countreq = denom

	@property
	def cardsleft(self):
		return denom-count
	@property
	def formatted(self):
		return "{}{}".format(cremojis[api2emoji(self.name)], self.level)

def goldcalc(self, cardlvl):
	allgold = 0
	for rarity in cardlvl:
		for lvl in cardlvl[rarity]:
			allgold += totalupgrades[rarity][lvl]
			# totalgold[rarity] += totalupgrades[rarity][lvl]
	return allgold

class Deck:
	def __init__(self, carddicts):
		self.cards = []
		for card in carddicts:
			c = Card(card['name'], card['rarity'], card['level'], card['count'], card['requiredForUpgrade'])
			self.cards.append(c)

	@property
	def goldspent(self):
		cardlvl = {'c': [], 'r':[],'e':[],'l':[]}
		for c in self.cards:
			cardlvl[c['rarity'][0]].append(c['level'])
		return goldcalc(cardlvl)
	@property
	def formatted(self):
		formdeck = []
		for c in self.cards:
			formdeck.append(c.formatted)
		return ' '.join(formdeck)

class CRGames:
	def __init__(self,s):
		self.total =  s['total'],
		self.tourney = s['tournamentGames'],
		self.wins = s['wins'],
		self.losses = s['losses'],
		self.draws = s['draws'],
		self.winstreak = s['currentWinStreak']
	@property
	def formatted(self):
		return [
			"Total Games: {}".format(self.total),
			"Tourney Games: {}".format(self.tourney),
			"Wins: {}".format(self.wins),
			"Losses: {}".format(self.losses),
			"Draws: {}".format(self.draws),
			"Current Win Streak: {}".format(self.winstreak)

		]

class CRStats:
	def __init__(self, s):
		self.legendtr = s['legendaryTrophies']
		self.tcardswon = s['tournamentCardsWon']
		self.cardswon = s['challengeCardsWon']
		self.pb = s['maxTrophies']
		self.crown3 = s['threeCrownWins']
		self.favcard = s['favoriteCard']
		self.donations = s['totalDonations']
		self.maxwins = s['challengeMaxWins']

	@property
	def formatted(self):
		return [
			"Legend Trophies: {}".format(self.legendtr),
			"Tourney Cards Won: {}".format(self.tcardswon),
			"Cards Won: {}".format(self.cardswon),
			"PB: {}{}".format(self.pb, cremojis['trophy']),
			"3 Crowns: {}".format(self.crown3),
			"Favorite Card: {}{}".format(self.favcard, cremojis[api2emoji(self.favcard)]),
			"Total Donations: {}".format(self.donations),
			"Max Wins: {}".format(self.maxwins)
		]

class CRChests:
	def __init__(self, s):
		self.pos = s['position']
		self.SMC = s['superMagicalPos']-self.pos
		self.legend = s['legendaryPos']-self.pos
		self.epic = s['epicPos']-self.pos

	@property
	def formatted(self):
		return [
			"Chests Opened: {}{}".format(self.pos,cremojis['chest']),
			"{}{}".format(cremojis['chestsupermagical'],self.SMC),
			"{}{}".format(cremojis['chestlegendary'],self.legend),
			"{}{}".format(cremojis['chestepic'],self.epic)
		]

class CROffers:
	def __init__(self,s):
		self.legend = s['legendary']
		self.epic = s['epic']
		self.arena = s['arena']
		self.units = ' days'
	@property
	def legendf(self):
		return str(self.legend) + self.units
	@property
	def epicf(self):
		return str(self.epic) + self.units
	@property
	def arenaf(self):
		return str(self.arena) + self.units
	#f means Formatted (with days)
	@property
	def formatted(self):
		return [
			"Legendary Offer: {}".format(self.legendf),
			"Epic Offer: {}".format(self.epicf),
			"Arena Offer: {}".format(self.arenaf)
		]


class CRSeasons:
	def __init__(self,s):
		self.seasons = s
		
	@property
	def formatted(self):
		formseasons = []
		for  s in self.seasons:
			formseasons.append("Season {0}: Ended at {1}{3}, PB {2}{3}".format(s['seasonNumber'],
				s['seasonEnding'],s['seasonHighest'],cremojis['trophy']))
		return '\n'.join(list(reversed(formseasons)))

class CRPlayer:


	def __init__(self):
		self.url = ''
		self.origindict = ''
		self.tag = ''
		self.name =''
		self.trophies =''
		self.arena =  ''
		self.namechangeleft = ''
		self.globalrank = ''
		self.clan = ''
		self.xp = ''
		self.stats ='' 
		self.games = ''
		self.chestcycle =''
		self.deck = ''
		self.seasons =''

	@classmethod
	async def create(self, tag):
		playerfulldict = {'norm':[], 'formatted':[ ]}
		self.url = crapiurl +'/profile/'+tag
		async with aiohttp.ClientSession() as session:
			async with session.get(self.url) as resp:
				datadict = await resp.json()
		formatted = CRPlayer()
		self.origindict = datadict
				
		self.tag = tag
		formatted.tag = '[{}]({})'.format(self.tag, self.url)
				
		self.name = datadict['name']
		formatted.name = datadict['name']
				
		self.trophies = datadict['trophies']
		formatted.trophies = "Trophies: {}{}".format(self.trophies, cremojis['trophy'])
				
		self.arena =  Arena(datadict['arena']['imageURL'], datadict['arena']['name'])
		formatted.arena = self.arena.formatted
				
		self.namechangeleft = not datadict['nameChanged']
		formatted.namechangeleft = "Can change name" if self.namechangeleft else "Can't Change Name"
				
		self.globalrank = datadict['globalRank']
		formatted.globalrank = "Global Rank: {}".format(self.globalrank) if self.globalrank != None  else ''
				
		self.clan = await CRClan.create(datadict['clan']['tag'])
		formatted.clan = "Clan: [{}]({})".format(self.clan.name, self.clan.url)
				
		self.xp = XP(datadict['experience']['xpRequiredForLevelUp'],datadict['experience']['xp'], datadict['experience']['level'])
		formatted.xp = self.xp.formatted

		self.stats = CRStats(datadict['stats'])
		formatted.stats = self.stats.formatted
		
		self.games = CRGames(datadict['games'])
		formatted.games = self.games.formatted
		
		self.chestcycle = CRChests(datadict['chestCycle'])
		formatted.chestcycle = self.chestcycle.formatted
		
		self.deck = Deck(datadict['currentDeck'])
		formatted.deck = self.deck.formatted
		
		self.seasons = CRSeasons(datadict['previousSeasons'])
		formatted.seasons = self.seasons.formatted
		return [self, formatted]

	@property
	def to_dict(self):
		return self.origindict

class InvalidRarity(Exception):
	pass
numcards = {}
numcards['c'] = 20
numcards['r'] = 21
numcards['e'] = 22
numcards['l'] = 13
maxcards = {
	'c':13,
	'r':11,
	'e':8,
	'l':5
}
tourneycards = {
	'c':9,
	'r':7,
	'e':4,
	'l':1
}


upgrades = {}
upgrades['c'] = [
	5,
	20,
	50,
	150,
	400,
	1000,
	2000,
	4000,
	8000,
	20000,
	50000,
	100000
]
upgrades['r'] = upgrades['c'][2:]
upgrades['e'] = upgrades['r'][3:]
upgrades['e'][upgrades['e'].index(1000)] = 400
upgrades['l'] = upgrades['e'][3:]
upgrades['l'][upgrades['l'].index(8000)] = 5000
for rarity in upgrades:
	upgrades[rarity].insert(0, 0)


totalupgrades = {}
for rarity in upgrades:
	totalupgrades[rarity] = []
	for index, cost in enumerate(upgrades[rarity]):
		totalupgrades[rarity].append(sum(upgrades[rarity][:index+1]))

class CRTags:

	def __init__(self, bot):
		
		self.settings = dataIO.load_json(SETTINGS_JSON)
		self.backsettings = dataIO.load_json(BACKSETTINGS_JSON)
		self.clansettings = dataIO.load_json(CLAN_JSON)
		self.bot = bot
		self.emojiservers = []

	@checks.is_owner()
	@commands.command(pass_context=True)
	async def cremojiinit(self, ctx):
		emojiservers = []
		for server in self.bot.servers:
			emojiservers.append(server)
		cremojis = {}
		for server in emojiservers:
			for emoji in server.emojis:
				cremojis[emoji.name] = "<:{}:{}>".format(emoji.name,emoji.id)
		dataIO.save_json(CREMOJIS_JSON, cremojis)
		await self.bot.say("Initialized")

	@commands.group(pass_context=True)
	async def clan(self, ctx):
		"""get clan info
		"""
		# racfserver = self.bot.get_server('218534373169954816')
		# await self.bot.say(racfserver.get_member('222925389641547776').mention)
		# await self.bot.say(server.get_member('222925389641547776').mention)
		# print(dir(CRClan('QUYCYV8')))
		if ctx.invoked_subcommand is None:
			await send_cmd_help(ctx)

	async def keyortag2tag(self, keyortag, ctx):
		originalkey = keyortag
		keyortag = keyortag.upper()
		members = list(ctx.message.server.members)
		membernames = []
		memberswithdiscrim = []
		for member in members:
			membernames.append(member.name)
			memberswithdiscrim.append(member.name + '#' + str(member.discriminator))
		userid = None
		tag = ''
		valid = True
		for letter in keyortag:
			if letter not in validChars:
				valid = False
				break
		if keyortag in self.clansettings:
			tag = self.clansettings[keyortag]
		elif valid:
			tag = keyortag
		elif keyortag.startswith('<@'): #assume mention
			userid = keyortag[2:-1]
			userid = userid.replace('!', '')
		elif keyortag.isdigit(): #assume userid
			userid = keyortag
		elif originalkey in members or originalkey in membernames or originalkey in memberswithdiscrim:	#if user in members
			for member in members:
				name = member.name
				if keyortag == member:
					userid = member.id
				elif keyortag == name:
					userid = member.id
					break
				elif keyortag == name + '#' + member.discriminator:
					userid = member.id
					break
		else:
			await self.bot.say('`{}` is not in the database, nor is an acceptable tag.'.format(keyortag))
			return
		if userid != None:
			try:
				usertag = self.settings[userid]
			except KeyError:
				await self.bot.say("That person is not in the database")
				return None
			player = await CRPlayer.create(usertag)			
			tag = player[0].clan.url.replace(crapi_url,'').replace('/clan/', '')
			print(tag)
		return tag

	@checks.mod_or_permissions()
	@clan.command(name='set', pass_context=True)
	async def clansettag(self, ctx, tag, *, key):
		author = ctx.message.author
		server = ctx.message.server
		author = server.get_member(author.id)
		rolenames = []
		for role in author.roles:
			rolenames.append(author.name)
		isbotcmder=False
		for role in rolenames:
			if role in BOTCMDER:
				isbotcmder = True
				break
		if checks.is_owner_check(ctx) or isbotcmder:
			pass
		else:
			return
		key = key.upper()
		tag = tag.upper()
		tag.replace('O', '0')
		valid = True
		for letter in tag:
			if letter not in validChars:
				valid = False
		if valid: #self.is_valid(tag):
			self.clansettings[key] = str(tag)
			dataIO.save_json(CLAN_JSON, self.clansettings)
			await self.bot.say("Saved {} for {}".format(tag, key))
		else:
			await self.bot.say("Invalid tag {}, it must only have the following characters {}".format(author.mention), validChars)
			
	@clan.command(name='get',pass_context=True)
	async def get_clan(self, ctx, keyortag=None):
		user = ctx.message.author
		if keyortag == None:
			keyortag = user.id
		tag = await self.keyortag2tag(keyortag, ctx)
		if tag == None:
			return
		clanurl = crapiurl + '/clan/' + tag
		await ctx.invoke(self.claninfo, tag)
		await ctx.invoke(self.clanroster, tag)
		return
		# await self.async_refresh(clanurl+ '/refresh')
		clan = await CRClan.create(tag)
		clan_data = []
		member_data = [] # for displaying all members 
		clan_data.append(clan.desc2)
		clan_data.append(clan.leader['formatted'])
		clan_data.append("Clan Tag: [`{}`]({})".format(tag, clan.clanurl))
		clan_data.append("Clan Score: [{}](http://)".format(clan.clan_trophy))
		clan_data.append("Trophy Requirement: [{}](http://)".format(clan.tr_req))
		# clan_data.append("")
		# n = 0
		# while n<len(clan.members):
		#     await self.bot.say(clan.members[n])
		#     n += 1
		# return
		members2display = clan.members
		n = 0
		members_per_embed = 13
		member_data = [] # for displaying all members
		while n<int(len(members2display)/members_per_embed+1):
			member_data.append([])
			n += 1

		n = 0
		while n<int(len(members2display)/members_per_embed+1):
			try:
				membersection = members2display[(n)*members_per_embed:(n+1)*members_per_embed]
			except:
				membersection = members2display[(n)*members_per_embed:]
			# await self.bot.say(membersection)
			for member in membersection:
				memberstring = member['formatted']
				member_data[n].append(memberstring)
			n += 1


		em = []

		if len(clan_data)>0:
			em.append(discord.Embed(url=clan.clanurl, title="{}".format(clan.name), description='\n'.join(clan_data),color = discord.Color(0x50d2fe)))
		for data in member_data:
			if len(em) == 0:
				em.append(discord.Embed(url=clan.clanurl, title="{}".format(clan.name), description='\n'.join(data),color = discord.Color(0x50d2fe)))
			else:
				em.append(discord.Embed(description='\n'.join(data),color = discord.Color(0x50d2fe)))
		try:
			discordname = user.name if user.nick is None else user.nick
		except:
			discordname = user.name
		em[0].set_author(icon_url=user.avatar_url,name=discordname)
		em[0].set_thumbnail(url=clan.clan_badge)
		em[len(em)-1].set_footer(text='Data provided by {}'.format(crapiurl.replace('api.', '', 1)), icon_url='https://raw.githubusercontent.com/cr-api/cr-api-docs/master/docs/img/cr-api-logo-b.png')


		for e in em:
			await self.bot.say(embed=e)


	@clan.command(name='roster',aliases=[],pass_context=True)
	async def clanroster(self, ctx, keyortag=None):
		user = ctx.message.author
		if keyortag == None:
			keyortag = user.id
		tag = await self.keyortag2tag(keyortag, ctx)
		if tag == None:
			return
		clanurl = crapiurl + '/clan/' + tag
		# await self.async_refresh(clanurl+ '/refresh')
		clan = await CRClan.create(tag)
		clan_data = []
		member_data = [] # for displaying all members 
		# clan_data.append(clan.desc2)
		# clan_data.append(clan.leader['formatted'])
		# clan_data.append("Clan Tag: [`{}`]({})".format(tag, clan.clan_url))
		# clan_data.append("Clan Score: [{}](http://)".format(clan.clan_trophy))
		# clan_data.append("Trophy Requirement: [{}](http://)".format(clan.tr_req))
		# clan_data.append("")
		# n = 0
		# while n<len(clan.members):
		#     await self.bot.say(clan.members[n])
		#     n += 1
		# return
		membertype = None
		members2display = clan.members
		if members2display != clan.members:
			membertype = members2display[0]['role']
		n = 0
		members_per_embed = 13
		member_data = [] # for displaying all members
		while n<int(len(members2display)/members_per_embed+1):
			member_data.append([])
			n += 1

		n = 0
		while n<int(len(members2display)/members_per_embed+1):
			try:
				membersection = members2display[(n)*members_per_embed:(n+1)*members_per_embed]
			except:
				membersection = members2display[(n)*members_per_embed:]
			# await self.bot.say(membersection)
			for member in membersection:
				memberstring = member['formatted']
				member_data[n].append(memberstring)
			n += 1


		em = []
		if membertype != None:
			currentdesc = "**{}** `{}s`\n".format(len(members2display), membertype)
		else:
			currentdesc = ''
		if len(clan_data)>0:
			# emtitle = clan.name
			# if membertype != None:
				# emtitle += '\n{} {}s'.format(len(members2display), membertype)
			e = discord.Embed(url=clan.clanurl, title="{}".format(clan.name), description='{}{}'.format(currentdesc, '\n'.join(data)),color = discord.Color(0x50d2fe))
			em.append(e)
		for data in member_data:
			if len(em) == 0:
				# emtitle = clan.name
				# if membertype != None:
				# 	emtitle += '\n{} {}s'.format(len(members2display), membertype)
				e = discord.Embed(url=clan.url, title="{}".format(clan.name), description='{}{}'.format(currentdesc, '\n'.join(data)),color = discord.Color(0x50d2fe))
				em.append(e)
				
			else:
				em.append(discord.Embed(description='\n'.join(data),color = discord.Color(0x50d2fe)))
		try:
			discordname = user.name if user.nick is None else user.nick
		except:
			discordname = user.name
		em[0].set_author(icon_url=user.avatar_url,name=discordname)
		# em[0].
		em[0].set_thumbnail(url=clan.badge)
		em[len(em)-1].set_footer(text='Data provided by {}'.format(crapi_url), icon_url='https://raw.githubusercontent.com/cr-api/cr-api-docs/master/docs/img/cr-api-logo-b.png')


		for e in em:
			await self.bot.say(embed=e)



	@clan.command(name='coleaders',aliases=['cos'],pass_context=True)
	async def clancoleaders(self, ctx, keyortag=None):
		user = ctx.message.author
		if keyortag == None:
			keyortag = user.id
		tag = await self.keyortag2tag(keyortag, ctx)
		if tag == None:
			return
		clanurl = crapiurl + '/clan/' + tag
		# await self.async_refresh(clanurl+ '/refresh')
		clan = await CRClan.create(tag)
		clan_data = []
		member_data = [] # for displaying all members 
		# clan_data.append(clan.desc2)
		# clan_data.append(clan.leader['formatted'])
		# clan_data.append("Clan Tag: [`{}`]({})".format(tag, clan.clan_url))
		# clan_data.append("Clan Score: [{}](http://)".format(clan.clan_trophy))
		# clan_data.append("Trophy Requirement: [{}](http://)".format(clan.tr_req))
		# clan_data.append("")
		# n = 0
		# while n<len(clan.members):
		#     await self.bot.say(clan.members[n])
		#     n += 1
		# return
		membertype = None
		members2display = clan.coleaders
		if members2display != clan.members:
			membertype = members2display[0]['role']
		n = 0
		members_per_embed = 13
		member_data = [] # for displaying all members
		while n<int(len(members2display)/members_per_embed+1):
			member_data.append([])
			n += 1

		n = 0
		while n<int(len(members2display)/members_per_embed+1):
			try:
				membersection = members2display[(n)*members_per_embed:(n+1)*members_per_embed]
			except:
				membersection = members2display[(n)*members_per_embed:]
			# await self.bot.say(membersection)
			for member in membersection:
				memberstring = member['formatted']
				member_data[n].append(memberstring)
			n += 1


		em = []
		if membertype != None:
			currentdesc = "**{}** `{}s`\n".format(len(members2display), membertype)
		else:
			currentdesc = ''
		if len(clan_data)>0:
			# emtitle = clan.name
			# if membertype != None:
				# emtitle += '\n{} {}s'.format(len(members2display), membertype)
			e = discord.Embed(url=clan.clanurl, title="{}".format(clan.name), description='{}{}'.format(currentdesc, '\n'.join(data)),color = discord.Color(0x50d2fe))
			em.append(e)
		for data in member_data:
			if len(em) == 0:
				# emtitle = clan.name
				# if membertype != None:
				# 	emtitle += '\n{} {}s'.format(len(members2display), membertype)
				e = discord.Embed(url=clan.url, title="{}".format(clan.name), description='{}{}'.format(currentdesc, '\n'.join(data)),color = discord.Color(0x50d2fe))
				em.append(e)
				
			else:
				em.append(discord.Embed(description='\n'.join(data),color = discord.Color(0x50d2fe)))
		try:
			discordname = user.name if user.nick is None else user.nick
		except:
			discordname = user.name
		em[0].set_author(icon_url=user.avatar_url,name=discordname)
		# em[0].
		em[0].set_thumbnail(url=clan.badge)
		em[len(em)-1].set_footer(text='Data provided by {}'.format(crapi_url), icon_url='https://raw.githubusercontent.com/cr-api/cr-api-docs/master/docs/img/cr-api-logo-b.png')


		for e in em:
			await self.bot.say(embed=e)



	@clan.command(name='elders',aliases=['elder'],pass_context=True)
	async def clanelders(self, ctx, keyortag=None):
		user = ctx.message.author
		if keyortag == None:
			keyortag = user.id
		tag = await self.keyortag2tag(keyortag, ctx)
		if tag == None:
			return
		clanurl = crapiurl + '/clan/' + tag
		# await self.async_refresh(clanurl+ '/refresh')
		clan = await CRClan.create(tag)
		clan_data = []
		member_data = [] # for displaying all members 
		# clan_data.append(clan.desc2)
		# clan_data.append(clan.leader['formatted'])
		# clan_data.append("Clan Tag: [`{}`]({})".format(tag, clan.clan_url))
		# clan_data.append("Clan Score: [{}](http://)".format(clan.clan_trophy))
		# clan_data.append("Trophy Requirement: [{}](http://)".format(clan.tr_req))
		# clan_data.append("")
		# n = 0
		# while n<len(clan.members):
		#     await self.bot.say(clan.members[n])
		#     n += 1
		# return
		membertype = None
		members2display = clan.elders
		if members2display != clan.members:
			membertype = members2display[0]['role']
		n = 0
		members_per_embed = 13
		member_data = [] # for displaying all members
		while n<int(len(members2display)/members_per_embed+1):
			member_data.append([])
			n += 1

		n = 0
		while n<int(len(members2display)/members_per_embed+1):
			try:
				membersection = members2display[(n)*members_per_embed:(n+1)*members_per_embed]
			except:
				membersection = members2display[(n)*members_per_embed:]
			# await self.bot.say(membersection)
			for member in membersection:
				memberstring = member['formatted']
				member_data[n].append(memberstring)
			n += 1


		em = []
		if membertype != None:
			currentdesc = "**{}** `{}s`\n".format(len(members2display), membertype)
		else:
			currentdesc = ''
		if len(clan_data)>0:
			# emtitle = clan.name
			# if membertype != None:
				# emtitle += '\n{} {}s'.format(len(members2display), membertype)
			e = discord.Embed(url=clan.clanurl, title="{}".format(clan.name), description='{}{}'.format(currentdesc, '\n'.join(data)),color = discord.Color(0x50d2fe))
			em.append(e)
		for data in member_data:
			if len(em) == 0:
				# emtitle = clan.name
				# if membertype != None:
				# 	emtitle += '\n{} {}s'.format(len(members2display), membertype)
				e = discord.Embed(url=clan.url, title="{}".format(clan.name), description='{}{}'.format(currentdesc, '\n'.join(data)),color = discord.Color(0x50d2fe))
				em.append(e)
				
			else:
				em.append(discord.Embed(description='\n'.join(data),color = discord.Color(0x50d2fe)))
		try:
			discordname = user.name if user.nick is None else user.nick
		except:
			discordname = user.name
		em[0].set_author(icon_url=user.avatar_url,name=discordname)
		# em[0].
		em[0].set_thumbnail(url=clan.badge)
		em[len(em)-1].set_footer(text='Data provided by {}'.format(crapi_url), icon_url='https://raw.githubusercontent.com/cr-api/cr-api-docs/master/docs/img/cr-api-logo-b.png')


		for e in em:
			await self.bot.say(embed=e)




	@clan.command(name='norole',aliases=[],pass_context=True)
	async def clannorole(self, ctx, keyortag=None):
		user = ctx.message.author
		if keyortag == None:
			keyortag = user.id
		tag = await self.keyortag2tag(keyortag, ctx)
		if tag == None:
			return
		clanurl = crapiurl + '/clan/' + tag
		# await self.async_refresh(clanurl+ '/refresh')
		clan = await CRClan.create(tag)
		clan_data = []
		member_data = [] # for displaying all members 
		# clan_data.append(clan.desc2)
		# clan_data.append(clan.leader['formatted'])
		# clan_data.append("Clan Tag: [`{}`]({})".format(tag, clan.clan_url))
		# clan_data.append("Clan Score: [{}](http://)".format(clan.clan_trophy))
		# clan_data.append("Trophy Requirement: [{}](http://)".format(clan.tr_req))
		# clan_data.append("")
		# n = 0
		# while n<len(clan.members):
		#     await self.bot.say(clan.members[n])
		#     n += 1
		# return
		membertype = None
		members2display = clan.members
		if members2display != clan.members:
			membertype = members2display[0]['role']
		n = 0
		members_per_embed = 13
		member_data = [] # for displaying all members
		while n<int(len(members2display)/members_per_embed+1):
			member_data.append([])
			n += 1

		n = 0
		while n<int(len(members2display)/members_per_embed+1):
			try:
				membersection = members2display[(n)*members_per_embed:(n+1)*members_per_embed]
			except:
				membersection = members2display[(n)*members_per_embed:]
			# await self.bot.say(membersection)
			for member in membersection:
				memberstring = member['formatted']
				member_data[n].append(memberstring)
			n += 1


		em = []
		if membertype != None:
			currentdesc = "**{}** `{}s`\n".format(len(members2display), membertype)
		else:
			currentdesc = ''
		if len(clan_data)>0:
			# emtitle = clan.name
			# if membertype != None:
				# emtitle += '\n{} {}s'.format(len(members2display), membertype)
			e = discord.Embed(url=clan.clanurl, title="{}".format(clan.name), description='{}{}'.format(currentdesc, '\n'.join(data)),color = discord.Color(0x50d2fe))
			em.append(e)
		for data in member_data:
			if len(em) == 0:
				# emtitle = clan.name
				# if membertype != None:
				# 	emtitle += '\n{} {}s'.format(len(members2display), membertype)
				e = discord.Embed(url=clan.url, title="{}".format(clan.name), description='{}{}'.format(currentdesc, '\n'.join(data)),color = discord.Color(0x50d2fe))
				em.append(e)
				
			else:
				em.append(discord.Embed(description='\n'.join(data),color = discord.Color(0x50d2fe)))
		try:
			discordname = user.name if user.nick is None else user.nick
		except:
			discordname = user.name
		em[0].set_author(icon_url=user.avatar_url,name=discordname)
		# em[0].
		em[0].set_thumbnail(url=clan.badge)
		em[len(em)-1].set_footer(text='Data provided by {}'.format(crapi_url), icon_url='https://raw.githubusercontent.com/cr-api/cr-api-docs/master/docs/img/cr-api-logo-b.png')


		for e in em:
			await self.bot.say(embed=e)


	@clan.command(name='info',pass_context=True)
	async def claninfo(self, ctx, keyortag=None):
		user = ctx.message.author
		if keyortag == None:
			keyortag = user.id
		elif keyortag.lower() == 'racf':
			for clan in racfclanslist:
				await ctx.invoke(self.claninfo, clan)
			return

		tag = await self.keyortag2tag(keyortag, ctx)
		if tag == None:
			return
		if tag == '':
			await self.bot.say("That user is not in a clan.")
			return
		clanurl = crapiurl + '/clan/' + tag
		# await self.async_refresh(clanurl+ '/refresh')
		clan = await CRClan.create(tag)
		clan_data = []
		member_data = [] # for displaying all members 
		clan_data.append(clan.desc2)
		clan_data.append(clan.leader['formatted'])
		clan_data.append("Clan Tag: [`{}`]({})".format(tag, clan.clanurl))
		clan_data.append("Clan Score: [{}](http://)".format(clan.clan_trophy))
		clan_data.append("Trophy Requirement: [{}](http://)".format(clan.tr_req))


		em = []

		if len(clan_data)>0:
			em.append(discord.Embed(url=clan.clanurl, title="{}".format(clan.name), description='\n'.join(clan_data),color = discord.Color(0x50d2fe)))
		for data in member_data:
			if len(em) == 0:
				em.append(discord.Embed(url=clan.clanurl, title="{}".format(clan.name), description='\n'.join(data),color = discord.Color(0x50d2fe)))
			else:
				em.append(discord.Embed(description='\n'.join(data),color = discord.Color(0x50d2fe)))
		try:
			discordname = user.name if user.nick is None else user.nick
		except:
			discordname = user.name
		em[0].set_author(icon_url=user.avatar_url,name=discordname)
		em[0].set_thumbnail(url=clan.clan_badge)
		em[len(em)-1].set_footer(text='Data provided by {}'.format(crapiurl.replace('api.', '', 1)), icon_url='https://raw.githubusercontent.com/cr-api/cr-api-docs/master/docs/img/cr-api-logo-b.png')

		for e in em:
			await self.bot.say(embed=e)


	def goldcalc(self, cardlvl):
		allgold = 0
		for rarity in cardlvl:
			for lvl in cardlvl[rarity]:
				allgold += totalupgrades[rarity][lvl]
				# totalgold[rarity] += totalupgrades[rarity][lvl]
		return allgold

	def lvlsdict(self, args):
		currentrarity = 'c'
		cardlvl = {
			'c':[],
			'r':[],
			'e':[],
			'l':[]
		}
		for x in args:
			if str(x).isalpha():
				if x in ['c', 'r', 'e', 'l']:
					currentrarity = x
				else:
					ex = InvalidRarity()
					raise ex
			elif str(x).isdigit():
				cardlvl[currentrarity].append(x)
		return cardlvl
	@commands.command(pass_context=True)
	async def gold(self, ctx, *, args):
		totalgold = {'c':0,'r':0,'e':0,'l':0,}
		allgold = 0
		cardlvl = {
			'c':[],
			'r':[],
			'e':[],
			'l':[]
		}
		msg = "It would cost a total of"
		msg2 = "gold to upgrade those cards"
		args = args.strip().split(' ')
		if 'max' in args:
			msg2 = "gold to upgrade all cards to max"
			args = []
			n = 0
			for rarity in numcards:
				args.append(rarity)
				while n < numcards[rarity]:
					args.append(str(maxcards[rarity]))
					n += 1
				n = 0
		if 'tourney' in args:
			msg2 = "gold to upgrade all cards to tourney standard"
			args = []
			n = 0
			for rarity in numcards:
				args.append(rarity)
				while n < numcards[rarity]:
					args.append(str(tourneycards[rarity]))
					n += 1
				n = 0
		if args.count('-') >1:
			await self.bot.say("too many minuses, limit is 1")
			return
		elif args.count('-') == 1:
			cardlvl = []
			allgold = []
			args = ' '.join(args).split('-')
			for index, arg in enumerate(args):
				args[index] = arg.strip().split(' ')
			for arg in args:
				while '' in arg:
					arg.remove('')

				for i, a in enumerate(arg):
					if a.isdigit():
						arg[i] = int(a)-1
			for arg in args:
				try:
					cardlvl.append(self.lvlsdict(arg))
				except InvalidRarity:
					await self.bot.say("Invalid Rarity")
			for c in cardlvl:
				try:
					allgold.append(self.goldcalc(c))
				except IndexError:
					await self.bot.say("Invalid card level")
			formattedgold = '{:,}'.format(allgold[0]-allgold[1])
		else:
			while '' in args:
				args.remove('')

			for i, a in enumerate(args):
				if a.isdigit():
					args[i] = int(a)-1
			currentrarity = 'c'
			try:
				cardlvl = self.lvlsdict(args)
			except InvalidRarity:
				await self.bot.say("Invalid Rarity")
				return
			try:
				allgold = self.goldcalc(cardlvl)
			except IndexError:
				await self.bot.say("Invalid card level")
			formattedgold = '{:,}'.format(allgold)
		await self.bot.say("{} {} {}".format(msg, formattedgold, msg2))
		# for rarity in totalgold:
		#     await self.bot.say("You have spent a total of {} gold on upgrading {} cards".format(totalgold[rarity], rarity))



	def statsvalid(self, tag):
		for letter in tag:
			if letter not in validChars:
				return False
		return True

	async def async_refresh(self,url):
		async with aiohttp.get(url) as r:
			response = await r.json()
			return response

	async def refresh(self, tag):
		await self.async_refresh('http://statsroyale.com/profile/'+tags[user.id]+'/refresh')

	@commands.command(pass_context=True)
	async def myid(self, ctx, user: discord.Member):
		"""show your discord ID"""
		if user == None:
			user=ctx.message.author
		await self.bot.say("ID: {}".format(user.id))
	
	@checks.is_owner()
	@commands.command(pass_context=True)
	async def copysettings2back(self, ctx):
		for x in self.settings:
			self.backsettings[self.settings[x]] = x
		print(self.backsettings)
		dataIO.save_json(BACKSETTINGS_JSON, self.backsettings)

	@checks.is_owner()
	@commands.command(pass_context=True)
	async def mergejsons(self, ctx):
		tags1 = dataIO.load_json(SETTINGS_JSON)
		tags2 = dataIO.load_json(SETTINGS2_JSON)
		tags3 = {}
		for x in tags1:
			tags3[x] = tags1[x]
		for x in tags2:
			tags3[x] = tags2[x]
		list3 = sorted(tags3)

		tags4 = {}
		for x in list3:
			tags4[x] = tags3[x]
		for x in tags4:
			self.settings[x] = tags4[x]
			dataIO.save_json(SET_JSON, self.settings)
		print(len(self.settings))
		dataIO.save_json(SET_JSON, self.settings)
		
	@checks.is_owner()
	@commands.command(name="cremojis",pass_context=True)
	async def _cremojis(self, ctx):
		
		await self.bot.say('penis')
		for emoji in cremojis:
			print(emoji)
		for emoji in cremojis:
			await self.bot.say(cremojis[emoji])

	@checks.is_owner()
	@commands.command(name="cremoji",pass_context=True)
	async def _cremoji(self, ctx, emojiname):
		try:
			await self.bot.say(self[emojiname])
		except KeyError:
			await self.bot.say("{} is not a saved cr emoji".format(emojiname))

	# @commands.command(aliases=['tra'], pass_context=True)
	# async def trapi(self,ctx,clan=None):
	# 	uclan = None
	# 	if clan != None:
	# 		uclan = clan.upper()
	# 	if clan == None:
	# 		clan = racfclanslist
	# 	elif uclan not in racfclans:
	# 		await self.bot.say("the clan, *\u200b{}* is not in racf".format(clan))
	# 		return
	# 	if type(clan) == type(['list']):
	# 		await self.bot.send_typing(ctx.message.channel)
	# 		em = discord.Embed(color=discord.Color(0xFF3844), title="RACF requirements:")
	# 		for c in clan:
	# 			for racfc in racfclanslist:
	# 				if racfc.lower() == c.lower():
	# 					goodcapsclan = racfc
	# 					break
	# 			tag = await self.keyortag2tag(c, ctx)
	# 			clan_data = await CRClan.create(tag)
	# 			trophyreq = await self.parsereq(clan_data.desc)
	# 			if trophyreq==None:
	# 				trophyreq = clan_data.tr_req
	# 			if goodcapsclan == 'eSports':
	# 				trophyreq = self['gitgud']
	# 			em.add_field(name="{}:".format(goodcapsclan), value=trophyreq)

	# 	else:
	# 		tag = await self.keyortag2tag(clan, ctx)
	# 		print("Tag: {}".format(tag))
	# 		clan_data = await CRClan.create(tag)
	# 		# clan_data.desc = "WE are reddit delta, we require a pb 4500 and our feeder is reddit echo"
	# 		#uncomment the above line to test the pb detection
	# 		trophyreq = await self.parsereq(clan_data.desc)
	# 		if trophyreq==None:
	# 			trophyreq = clan_data.tr_req
	# 		for c in racfclanslist:
	# 			if c.lower() == clan.lower():
	# 				goodcapsclan = c
	# 				break
	# 		if goodcapsclan == 'eSports':
	# 			trophyreq = self['gitgud']
	# 		em = discord.Embed(color=discord.Color(0xFF3844), title="{} trophy req:".format(goodcapsclan), description=trophyreq)

	# 	await self.bot.say(embed=em)

	# async def parsereq(self, desc):
	# 	trophynums = []
	# 	n = 0
	# 	for l in desc:
	# 		try:
	# 			if l.isdigit() or (l.lower()=='p' and desc[n+1].lower()=='b')or (l.lower()=='b' and desc[n-1].lower()=='p') or l.lower() == 'o':
	# 				trophynums.append(l)
	# 			elif trophynums[len(trophynums)-1] != " ":
	# 				trophynums.append(' ')
	# 		except IndexError:
	# 			pass
	# 		n+=1
	# 	n = 0
	# 	trnums = ''.join(trophynums)
	# 	trnums = trnums.split(' ')
	# 	while n<len(trnums):
	# 		d = trnums[n]
	# 		# print("trnums: {}".format(trnums))
	# 		# print("{}, len: {}".format(d, len(d)))
	# 		if len(d) == 4 or d.lower() =='pb':
	# 			if d.isdigit():
	# 				trnums[n] = "{:,}".format(int(d))
	# 			n += 1
	# 		else:
	# 			trnums.remove(d)
	# 	print(trnums)
	# 	print(len(trnums))
	# 	n = 0
	# 	for d in trnums:
	# 		trnums[n] = trnums[n].replace('O', '0').replace('o', '0')
	# 		n += 1
	# 	trophyreq = None
	# 	if len(trnums)==0:
	# 		trnums = None
	# 	elif len(trnums) == 1:
	# 		trnums = trnums[0]
	# 	elif len(trnums)==2:
	# 		n = 0
	# 		while n<len(trnums):
	# 			if trnums[n].isdigit():
	# 				trnums[n] = "{:,}".format(int(d))
	# 			n+=1
	# 		trnums = ' '.join(trnums)
	# 	parseddesc = trnums
	# 	if parseddesc == None:
	# 		trophyreq = None
	# 	if type(parseddesc) == type('string'):
	# 		trophyreq = parseddesc
	# 	elif type(parseddesc) == type(['list']):
	# 		trreqs =''
	# 		n = 0
	# 		for d in parseddesc:
	# 			trreqs +=d 
	# 			# print("parseddesc len: {}\nn: {}\nnextone: {}".format(len(parseddesc) ,n, parseddesc[n+1].lower()))
	# 			try:
	# 				if n !=len(parseddesc)-1 and parseddesc[n+1].lower()!='pb':
	# 					trreqs += ', '
	# 				else:
	# 					trreqs += ' '
	# 			except IndexError:
	# 				pass
	# 			n+=1
	# 		trophyreq = trreqs
	# 	return trophyreq



	@commands.group(aliases=["stats"], pass_context=True)
	async def clashroyale(self, ctx):
		"""Display CR profiles."""
		if ctx.invoked_subcommand is None:
			await send_cmd_help(ctx)

	def savetag(self, userid, tag):
		try:
			if not userid.isdigit():
				print("must save userid, tag not backwards")
				return
		except:
			return
		self.settings[userid] = str(tag)
		for t in self.backsettings:
			if self.backsettings[t] == userid:
				self.backsettings.pop(t, None)
				break
		self.backsettings[str(tag)] = userid
		dataIO.save_json(SETTINGS_JSON, self.settings)
		dataIO.save_json(BACKSETTINGS_JSON, self.backsettings)

	def deltag(self, userid, tag):
		try:
			if not userid.isdigit():
				print("must del userid, tag not backwards")
				return
		except:
			return
		for t in self.backsettings:
			if self.backsettings[t] == userid:
				self.backsettings.pop(t, None)
				break
		self.settings.pop(userid, None)
		dataIO.save_json(SETTINGS_JSON, self.settings)
		dataIO.save_json(BACKSETTINGS_JSON, self.backsettings)

	@commands.command(pass_context=True)
	async def crsendjson(self, ctx):
		heroku = False
		if 'DYNO_RAM' in os.environ:
			heroku = True
		if heroku:
			await self.bot.send_file(destination=ctx.message.channel, fp=r"/app/data/crtags/settings.json", filename="settings.json")
			await self.bot.send_file(destination=ctx.message.channel, fp=r"/app/data/crtags/backsettings.json", filename="backsettings.json")
			await self.bot.send_file(destination=ctx.message.channel, fp=r"/app/data/crtags/clan.json", filename="clan.json")
		else:
			await self.bot.send_file(destination=ctx.message.channel, fp=r"data\crtags\settings.json", filename="settings.json")
			await self.bot.send_file(destination=ctx.message.channel, fp=r"data\crtags\backsettings.json", filename="backsettings.json")
			await self.bot.send_file(destination=ctx.message.channel, fp=r"data\crtags\clan.json", filename="clan.json")
			# os.environ['playersettings'] = self.settings

			
	@clashroyale.command(name='get', pass_context=True)
	async def gettag(self, ctx, user: discord.Member=None):
		"""Get user tag. If not given a user, get author's tag"""
		if user == None:
			user = ctx.message.author
		tags = dataIO.load_json(SETTINGS_JSON)
		try:
			test = tags[user.id]
		except(KeyError):
			await self.bot.say("{} does not have a tag set.".format(user.display_name))
			return
		if(user==None):
			if tags[ctx.message.author.id]:
				await self.bot.say("Your tag is {}.".format(tags[ctx.message.author.id]))
			else:
				await self.bot.say("You, {} do not have a tag set.".format(ctx.message.author.display_name))
		else:
			if tags[user.id]:
				await self.bot.say("{}'s tag is {}.".format(user.mention, tags[user.id]))
			else:
				await self.bot.say("User {} does not have a tag set.".format(user.display_name))


	@clashroyale.command(aliases=['set'],pass_context=True)
	async def settag(self, ctx, tag):
		"""Save user tag. If not given a user, save tag to author"""
		author = ctx.message.author
		tag = tag.upper()
		tag.replace('O', '0')
		valid = True
		for letter in tag:
			if letter not in validChars:
				valid = False
		if valid: #self.is_valid(tag):
			self.savetag(author.id, tag)
			await self.bot.say("Saved {} for {}".format(tag, author.display_name))
		else:
			await self.bot.say("Invalid tag {}, it must only have the following characters {}".format(author.mention, validChars))

	@clashroyale.command(name='deltag',aliases=['del'],pass_context=True)
	async def _deltag(self, ctx):
		"""Delete user tag."""
		author = ctx.message.author
		valid = True
		self.deltag(author.id, self.settings[author.id])
		await self.bot.say("deleted tag from {}".format( author.display_name))

	@checks.mod_or_permissions()
	@clashroyale.command(pass_context=True)
	async def setusertag(self, ctx, user: discord.Member, tag):
		"""Save user tag. If not given a user, save tag to author"""
		if user == None:
			user = ctx.message.author
		tag = tag.upper()
		tag.replace('O', '0')
		valid = True
		for letter in tag:
			if letter not in validChars:
				valid = False
		if valid: #self.is_valid(tag):
			author = ctx.message.author
			await self.bot.say("Saving {} for {}".format(tag, user.display_name))
			self.savetag(user.id, tag)
		else:
			await self.bot.say("Invalid tag {}, it must only have the following characters {}".format(ctx.message.author.mention, validChars))
	async def keyortag2tag2(self,userortag,ctx):
		tags = dataIO.load_json(SETTINGS_JSON)
		print(userortag)
		tag = None
		userid = None
		valid=False
		if userortag != None:
			valid = True
			for letter in userortag.upper():
				if letter not in validChars:
					valid = False
		if userortag == None: #assume author if none
			userid = ctx.message.author.id
		elif userortag.startswith('<@'): #assume mention
			print(userid)
			userid = userortag[2:-1]
		elif userortag.isdigit(): #assume userid
			userid = userortag
		elif valid: #assume it is a tag
			tag = userortag.upper()
		else:	#assume member name
			for member in list(ctx.message.server.members):
				name = member.name
				if userortag == name:
					userid = member.id
				elif userortag == name + '#' + member.discriminator:
					userid = member.id
		if userid != None:
			user = await self.bot.get_user_info(userid)
				
		if tag == None:
			if userid in tags:
				tag = tags[userid]
			else:
				await self.bot.say("{} does not have a tag set.".format(user.display_name))
				return None
		return [tag, user]

	@clashroyale.command(name='trophy', aliases=['tr'],  pass_context=True)
	async def _trophy(self, ctx, userortag=None):
		"""Get user trophies. If not given a user, get author's data"""
		tag = await self.keyortag2tag2(userortag, ctx)
		if tag == None:
			return
		if tag[0] == None:
			return
		user = tag[1]
		tag = tag[0]
		player = await CRPlayer.create(tag)
		fplayer = player[1]
		player = player[0]
		elements = []
		player_data = []
		print(dir(fplayer))

		elements2display  = [
			'tag',
			'clan',
			'trophies',
			'stats',
			'chestcycle',
			'seasons',
			'xp',
			'deck'
		]
		# print('{}\n{}'.format(fplayer.stats, type(fplayer.stats)))
		for ele in elements2display:
			thing = eval('fplayer.{}'.format(ele))
			print(type(thing)==type([]))
			print(thing)
			print('\n')
			# print('i am {}'.format(type(thing)))
			if type(thing) == type(['list']):
				eval("player_data.extend(fplayer.{})".format(ele))
			else:
				thing = str(thing)
				eval("player_data.append(fplayer.{})".format(ele))

		em = discord.Embed(title=player.name, description='\n'.join(player_data),color = discord.Color(0x50d2fe))
		try:
			discordname = user.name if user.nick is None else user.nick
		except:
			discordname = user.name
		em.set_author(icon_url=user.avatar_url,name=discordname)
		em.set_thumbnail(url=player.clan.badge)
		em.set_footer(text='Data provided by CR-API', icon_url='https://i.imgur.com/Grj2j6D.png')
		await self.bot.say(embed=em)

		
	@clashroyale.command(name='chests',  pass_context=True)
	async def _chests(self, ctx, userortag=None):
		"""Get user trophies. If not given a user, get author's data"""
		tags = dataIO.load_json(SETTINGS_JSON)
		tag = None
		userid = None
		valid=False
		if userortag != None:
			valid = True
			for letter in userortag.upper():
				if letter not in validChars:
					valid = False
		if userortag == None: #assume author if none
			userid = ctx.message.author.id
		elif userortag.startswith('<@'): #assume mention
			userid = userortag[2:-1]
		elif userortag.isdigit(): #assume userid
			userid = userortag
		elif valid: #assume it is a tag
			tag = userortag.upper()
		else:	#assume member name
			for member in list(ctx.message.server.members):
				name = member.name
				if userortag == name:
					userid = member.id
				elif userortag == name + '#' + member.discriminator:
					userid = member.id
		if userid != None:
			user = ctx.message.server.get_member(userid)
		if tag == None:
			if userid in tags:
				tag = tags[userid]
			else:
				await self.bot.say("{} does not have a tag set.".format(user.display_name))
				return
		
		user_url = (statscr_url+ tag)
		things = await CRPlayer.create(tag)
		player_data  = []
		player_data.append('[{}]({})'.format(tag, user_url))
		# player_data.append(things.pb)
		# player_data.append(things.trophy)
		# player_data.append(things.cardswon)
		# player_data.append(things.tcardswon)
		# player_data.append(things.donations)
		# player_data.append(things.prevseasonrank)
		# player_data.append(things.prevseasontrophy)
		# player_data.append(things.prevseasonpb)
		# player_data.append(things.wins)
		# player_data.append(things.losses)
		# player_data.append(things.crown3)
		# player_data.append(things.league)
		player_data.append(things.chests)
		em = discord.Embed(title=things.name, description='\n'.join(player_data),color = discord.Color(0x50d2fe))
		try:
			discordname = user.name if user.nick is None else user.nick
		except:
			discordname = user.name
		em.set_author(icon_url=user.avatar_url,name=discordname)
		em.set_thumbnail(url=things.clan_badge)
		em.set_footer(text='Data provided by StatsRoyale', icon_url='http://i.imgur.com/17R3DVU.png')
		await self.bot.say(embed=em)


	@clashroyale.command(name='cardswon', aliases=['cards'],  pass_context=True)
	async def _cardswon(self, ctx, userortag=None):
		"""Get user trophies. If not given a user, get author's data"""
		tags = dataIO.load_json(SETTINGS_JSON)
		tag = None
		userid = None
		valid=False
		if userortag != None:
			valid = True
			for letter in userortag.upper():
				if letter not in validChars:
					valid = False
		if userortag == None: #assume author if none
			userid = ctx.message.author.id
		elif userortag.startswith('<@'): #assume mention
			userid = userortag[2:-1]
		elif userortag.isdigit(): #assume userid
			userid = userortag
		elif valid: #assume it is a tag
			tag = userortag.upper()
		else:	#assume member name
			for member in list(ctx.message.server.members):
				name = member.name
				if userortag == name:
					userid = member.id
				elif userortag == name + '#' + member.discriminator:
					userid = member.id
		if userid != None:
			user = ctx.message.server.get_member(userid)
		if tag == None:
			if userid in tags:
				tag = tags[userid]
			else:
				await self.bot.say("{} does not have a tag set.".format(user.display_name))
				return
		
		user_url = (statscr_url+ tag)
		things = await CRPlayer.create(tag)
		player_data  = []
		player_data.append('[{}]({})'.format(tag, user_url))
		# player_data.append(things.pb)
		# player_data.append(things.trophy)
		player_data.append(things.cardswon)
		player_data.append(things.tcardswon)
		# player_data.append(things.donations)
		# player_data.append(things.prevseasonrank)
		# player_data.append(things.prevseasontrophy)
		# player_data.append(things.prevseasonpb)
		# player_data.append(things.wins)
		# player_data.append(things.losses)
		# player_data.append(things.crown3)
		# player_data.append(things.league)
		player_data.append(things.chests)
		em = discord.Embed(title=things.name, description='\n'.join(player_data),color = discord.Color(0x50d2fe))
		try:
			discordname = user.name if user.nick is None else user.nick
		except:
			discordname = user.name
		em.set_author(icon_url=user.avatar_url,name=discordname)
		em.set_thumbnail(url=things.clan_badge)
		em.set_footer(text='Data provided by StatsRoyale', icon_url='http://i.imgur.com/17R3DVU.png')
		await self.bot.say(embed=em)


	@clashroyale.command(pass_context=True)
	async def profile(self, ctx, userortag=None):
		"""Get user trophies. If not given a user, get author's data"""
		tags = dataIO.load_json(SETTINGS_JSON)
		tag = None
		userid = None
		valid=False
		if userortag != None:
			valid = True
			for letter in userortag.upper():
				if letter not in validChars:
					valid = False
		if userortag == None: #assume author if none
			userid = ctx.message.author.id
		elif userortag.startswith('<@'): #assume mention
			userid = userortag[2:-1]
		elif userortag.isdigit(): #assume userid
			userid = userortag
		elif valid: #assume it is a tag
			tag = userortag.upper()
		else:	#assume member name
			for member in list(ctx.message.server.members):
				name = member.name
				if userortag == name:
					userid = member.id
				elif userortag == name + '#' + member.discriminator:
					userid = member.id
		if userid != None:
			user = ctx.message.server.get_member(userid)
		if tag == None:
			if userid in tags:
				tag = tags[userid]
			else:
				await self.bot.say("{} does not have a tag set.".format(user.display_name))
				return
		
		user_url = (statscr_url+ tag)
		things = await CRPlayer.create(tag)
		player_data  = []
		player_data.append('[{}]({})'.format(tag, user_url))
		if things.clan_url != '':
			player_data.append('[{}]({})'.format(things.clan,things.clan_url))
		else:
			player_data.append('{}'.format(things.clan))
		player_data.append(things.pb)
		player_data.append(things.trophy)
		player_data.append(things.cardswon)
		player_data.append(things.tcardswon)
		player_data.append(things.donations)
		player_data.append(things.prevseasonrank)
		player_data.append(things.prevseasontrophy)
		player_data.append(things.prevseasonpb)
		player_data.append(things.wins)
		player_data.append(things.losses)
		player_data.append(things.crown3)
		player_data.append(things.league)
		# player_data.append(things.chests)
		em = discord.Embed(title=things.name, description='\n'.join(player_data),color = discord.Color(0x50d2fe))
		try:
			discordname = user.name if user.nick is None else user.nick
		except:
			discordname = user.name
		em.set_author(icon_url=user.avatar_url,name=discordname)
		em.set_thumbnail(url=things.clan_badge)
		em.set_footer(text='Data provided by StatsRoyale', icon_url='http://i.imgur.com/17R3DVU.png')
		await self.bot.say(embed=em)

	@clashroyale.command(name='pb', pass_context=True)
	async def _pb(self, ctx, userortag=None):
		"""Get user trophies. If not given a user, get author's data"""
		tags = dataIO.load_json(SETTINGS_JSON)
		tag = None
		userid = None
		valid=False
		if userortag != None:
			valid = True
			for letter in userortag.upper():
				if letter not in validChars:
					valid = False
		if userortag == None: #assume author if none
			userid = ctx.message.author.id
		elif userortag.startswith('<@'): #assume mention
			userid = userortag[2:-1]
		elif userortag.isdigit(): #assume userid
			userid = userortag
		elif valid: #assume it is a tag
			tag = userortag.upper()
		else:	#assume member name
			for member in list(ctx.message.server.members):
				name = member.name
				if userortag == name:
					userid = member.id
				elif userortag == name + '#' + member.discriminator:
					userid = member.id
		if userid != None:
			user = ctx.message.server.get_member(userid)
		if tag == None:
			if userid in tags:
				tag = tags[userid]
			else:
				await self.bot.say("{} does not have a tag set.".format(user.display_name))
				return
		
		user_url = (statscr_url+ tag)
		things = await CRPlayer.create(tag)
		player_data  = []
		player_data.append('[{}]({})'.format(tag, user_url))
		player_data.append(things.pb)
		# player_data.append(things.trophy)
		# player_data.append(things.cardswon)
		# player_data.append(things.tcardswon)
		# player_data.append(things.donations)
		# player_data.append(things.prevseasonrank)
		# player_data.append(things.prevseasontrophy)
		# player_data.append(things.prevseasonpb)
		# player_data.append(things.wins)
		# player_data.append(things.losses)
		# player_data.append(things.crown3)
		# player_data.append(things.league)
		# player_data.append(things.chests)
		em = discord.Embed(title=things.name, description='\n'.join(player_data),color = discord.Color(0x50d2fe))
		try:
			discordname = user.name if user.nick is None else user.nick
		except:
			discordname = user.name
		em.set_author(icon_url=user.avatar_url,name=discordname)
		em.set_thumbnail(url=things.clan_badge)
		em.set_footer(text='Data provided by StatsRoyale', icon_url='http://i.imgur.com/17R3DVU.png')
		await self.bot.say(embed=em)

	

def check_folder():
	if not os.path.exists(PATH):
		os.makedirs(PATH)

def check_file():
	defaults = {}
	if not dataIO.is_valid_json(SETTINGS_JSON):
		dataIO.save_json(SETTINGS_JSON, defaults)
	if not dataIO.is_valid_json(CLAN_JSON):
		dataIO.save_json(CLAN_JSON, defaults)
	if not dataIO.is_valid_json(BACKSETTINGS_JSON):
		dataIO.save_json(BACKSETTINGS_JSON, defaults)
	if not dataIO.is_valid_json(CREMOJIS_JSON):
		dataIO.save_json(CREMOJIS_JSON, defaults)

def setup(bot):
	check_folder()
	check_file()
	bot.add_cog(CRTags(bot))