import json, sys, sqlite3, copy, urllib2

def fixItems(itemDict):
	itemDict["3280"] = itemDict["1309"]
	itemDict["3282"] = itemDict["1305"]
	itemDict["3281"] = itemDict["1307"]
	itemDict["3284"] = itemDict["1306"]
	itemDict["3283"] = itemDict["1308"]
	itemDict["3278"] = itemDict["1333"]
	itemDict["3279"] = itemDict["1331"]
	itemDict["3250"] = itemDict["1304"]
	itemDict["3251"] = itemDict["1302"]
	itemDict["3254"] = itemDict["1301"]
	itemDict["3255"] = itemDict["1314"]
	itemDict["3252"] = itemDict["1300"]
	itemDict["3253"] = itemDict["1303"]
	itemDict["3263"] = itemDict["1318"]
	itemDict["3264"] = itemDict["1316"]
	itemDict["3265"] = itemDict["1324"]
	itemDict["3266"] = itemDict["1322"]
	itemDict["3260"] = itemDict["1319"]
	itemDict["3261"] = itemDict["1317"]
	itemDict["3262"] = itemDict["1315"]
	itemDict["3257"] = itemDict["1310"]
	itemDict["3256"] = itemDict["1312"]
	itemDict["3259"] = itemDict["1311"]
	itemDict["3258"] = itemDict["1313"]
	itemDict["3276"] = itemDict["1332"]
	itemDict["3277"] = itemDict["1330"]
	itemDict["3274"] = itemDict["1326"]
	itemDict["3275"] = itemDict["1334"]
	itemDict["3272"] = itemDict["1325"]
	itemDict["3273"] = itemDict["1328"]
	itemDict["3270"] = itemDict["1329"]
	itemDict["3271"] = itemDict["1327"]
	itemDict["3269"] = itemDict["1321"]
	itemDict["3268"] = itemDict["1323"]
	itemDict["3267"] = itemDict["1320"]
	return itemDict

# put api key into file to protect it
def loadAPIKey():
	with open("apiKey.txt") as f:
		for line in f:
			# first line is api key
			return str(line.strip())

def loadDict(filename):
	newDict = {}
	with open(filename) as f:
		for line in f:
			line = line.strip()
			line = line.split("::") # our delimiter
			key = line[0]
			val = line[1]
			newDict[key] = val
	return newDict

def sumOfItems(champStats, patch, itemId):
	return champStats[patch]["NA"][key] + champStats[patch]["BR"][key] + champStats[patch]["EUNE"][key] + champStats[patch]["EUW"][key] + champStats[patch]["KR"][key]

def sumOfKey(champStats, patch, key):
	return champStats[patch]["NA"][key] + champStats[patch]["BR"][key] + champStats[patch]["EUNE"][key] + champStats[patch]["EUW"][key] + champStats[patch]["KR"][key]

if __name__ == '__main__':
	#if(len(sys.argv) < 2):
	#	print("Please run with a champion id to generate data for.")
	apiKey = loadAPIKey()
	processedChamps = set()
	with open("processedChamps.txt") as f:
		for line in f:
			line = line.strip()
			processedChamps.add(line)
		f.close()

	itemDict = loadDict("itemData.txt")
	itemDict = fixItems(itemDict)
	champDict = loadDict("champData.txt")

	#champId = sys.argv[1]

	databases = [
		["5.11", "NA", "Databases/5.11/Ranked/NA.db"], 
		["5.11", "BR", "Databases/5.11/Ranked/BR.db"], 
		["5.11", "EUNE", "Databases/5.11/Ranked/EUNE.db"],
		["5.11", "EUW", "Databases/5.11/Ranked/EUW.db"],
		["5.11", "KR", "Databases/5.11/Ranked/KR.db"],
		["5.14", "NA", "Databases/5.14/Ranked/NA.db"],
		["5.14", "BR", "Databases/5.14/Ranked/BR.db"],
		["5.14", "EUNE", "Databases/5.14/Ranked/EUNE.db"],
		["5.14", "EUW", "Databases/5.14/Ranked/EUW.db"],
		["5.14", "KR", "Databases/5.14/Ranked/KR.db"],
	]

	defaultItems = {}
	for itemId in itemDict:
		defaultItems[int(itemId)] = 0

	defaultChamps = {}
	for chId in champDict:
		defaultChamps[int(chId)] = 0

	defaultStats = {
		"gamesPlayed": 0,
		"gamesCarried": 0,
		"items": copy.deepcopy(defaultItems),
		"champs": copy.deepcopy(defaultChamps),
		"kills": 0,
		"deaths": 0,
		"assists": 0,
		"kda": 0,
		"damage": 0,
		"killPart": 0,
		"damagePerc": 0
	}

	defaultObj = {
		"total": copy.deepcopy(defaultStats),
		"BR": copy.deepcopy(defaultStats),
		"EUNE": copy.deepcopy(defaultStats),
		"EUW": copy.deepcopy(defaultStats),
		"NA": copy.deepcopy(defaultStats),
		"KR": copy.deepcopy(defaultStats)
	}

	for champId in champDict: 
		if(champId in processedChamps):
			print("Champion " + champId + " already processed. Skipping.")
			continue
		champStats = {
			"title": "",
			"name": "",
			"5.11": copy.deepcopy(defaultObj),
			"5.14": copy.deepcopy(defaultObj)	
		}
		print("Advancing to champ " + champId)
		url = "https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion/" + champId + "?api_key=" + apiKey
		# simple API request to get response as plaintext
		try:
			content = urllib2.urlopen(url)
		except urllib2.HTTPError, e:
			if(e.code != 200):
				print("Error in API request for champion " + champId + " :(    " + str(e.code))
				continue
		response = str(content.read()) # str() so that it is not unicode
		# convert response to json
		response = json.loads(response)
		champStats["title"] = response["title"]
		champStats["name"] = response["name"]
		for dbInfo in databases:
			# Just chose this order to have all variables conveniently
			patch = dbInfo[0]
			region = dbInfo[1]
			filename = dbInfo[2]
			print("Advancing to database: " + filename)
			db = sqlite3.connect(filename)
			cursor = db.cursor()
			cursor.execute("SELECT count(*) from players where championId=" + champId)
			rows = cursor.fetchall()
			count = rows[0][0] # first row, tuple of just one value
			champStats[patch][region]["gamesPlayed"] = count

			cursor.execute("SELECT count(*) from players where carried=1 and championId=" + champId)
			rows = cursor.fetchall()
			count = rows[0][0] # first row, tuple of just one value
			champStats[patch][region]["gamesCarried"] = count

			cursor.execute("SELECT item0, item1, item2, item3, item4, item5, item6, kills, deaths, assists, totalDamage, killPart, damagePerc from players where carried=1 and championId=" + champId)
			rows = cursor.fetchall()
			for row in rows:
				items = row[:7]
				for itemId in items:
					if(itemId == 0):
						continue
					if itemId in champStats[patch][region]["items"]:
						champStats[patch][region]["items"][itemId] += 1

				kills = row[7]
				deaths = row[8]
				assists = row[9]
				damage = row[10]
				killPart = row[11]
				damagePerc = row[12]

				champStats[patch][region]["kills"] += kills
				champStats[patch][region]["deaths"] += deaths
				champStats[patch][region]["assists"] += assists
				champStats[patch][region]["damage"] += damage
				champStats[patch][region]["killPart"] += killPart
				champStats[patch][region]["damagePerc"] += damagePerc
			if(champStats[patch][region]["deaths"] == 0):
				champStats[patch][region]["kda"] = 100
			else:
				champStats[patch][region]["kda"] = float(champStats[patch][region]["kills"] + champStats[patch][region]["assists"]) / champStats[patch][region]["deaths"]
			gamesCarried = float(champStats[patch][region]["gamesCarried"])
			if(champStats[patch][region]["gamesCarried"] > 0):
				champStats[patch][region]["kills"] /= gamesCarried
				champStats[patch][region]["deaths"] /= gamesCarried
				champStats[patch][region]["assists"] /= gamesCarried
				champStats[patch][region]["damage"] /= gamesCarried
				champStats[patch][region]["killPart"] /= gamesCarried
				champStats[patch][region]["damagePerc"] /= gamesCarried

			cursor.execute("SELECT matchId, teamId from players where carried=1 and championId=" + champId)
			rows = cursor.fetchall()
			for row in rows:
				matchId = row[0]
				teamId = row[1]
				cursor.execute("SELECT championId from players where matchId=" + str(matchId) + " and teamId=" + str(teamId))
				newRows = cursor.fetchall()
				for newRow in newRows:
					championId = newRow[0]
					champStats[patch][region]["champs"][championId] += 1

			db.close()
			
		###################################################
		# populate the total fields of 5.11 and 5.14 here #
		###################################################
		champStats["5.11"]["total"]["gamesPlayed"] = sumOfKey(champStats, "5.11", "gamesPlayed")
		champStats["5.11"]["total"]["gamesCarried"] = sumOfKey(champStats, "5.11", "gamesCarried")
		champStats["5.11"]["total"]["kills"] = sumOfKey(champStats, "5.11", "kills") / 5.0 # since 5 regions
		champStats["5.11"]["total"]["deaths"] = sumOfKey(champStats, "5.11", "deaths") / 5.0
		champStats["5.11"]["total"]["assists"] = sumOfKey(champStats, "5.11", "assists") / 5.0
		champStats["5.11"]["total"]["kda"] = sumOfKey(champStats, "5.11", "kda") / 5.0
		champStats["5.11"]["total"]["damage"] = sumOfKey(champStats, "5.11", "damage") / 5.0
		champStats["5.11"]["total"]["killPart"] = sumOfKey(champStats, "5.11", "killPart") / 5.0
		champStats["5.11"]["total"]["damagePerc"] = sumOfKey(champStats, "5.11", "damagePerc") / 5.0
		for itemId in champStats["5.11"]["total"]["items"]:
			champStats["5.11"]["total"]["items"][itemId] = champStats["5.11"]["NA"]["items"][itemId] + champStats["5.11"]["BR"]["items"][itemId] \
			+ champStats["5.11"]["EUW"]["items"][itemId] + champStats["5.11"]["KR"]["items"][itemId] + champStats["5.11"]["EUNE"]["items"][itemId]
		for chId in champStats["5.11"]["total"]["champs"]:
			champStats["5.11"]["total"]["champs"][chId] = champStats["5.11"]["NA"]["champs"][chId] + champStats["5.11"]["BR"]["champs"][chId] \
			+ champStats["5.11"]["EUW"]["champs"][chId] + champStats["5.11"]["KR"]["champs"][chId] + champStats["5.11"]["EUNE"]["champs"][chId]

		champStats["5.14"]["total"]["gamesPlayed"] = sumOfKey(champStats, "5.14", "gamesPlayed")
		champStats["5.14"]["total"]["gamesCarried"] = sumOfKey(champStats, "5.14", "gamesCarried")
		champStats["5.14"]["total"]["kills"] = sumOfKey(champStats, "5.14", "kills") / 5.0 # since 5 regions
		champStats["5.14"]["total"]["deaths"] = sumOfKey(champStats, "5.14", "deaths") / 5.0
		champStats["5.14"]["total"]["assists"] = sumOfKey(champStats, "5.14", "assists") / 5.0
		champStats["5.14"]["total"]["kda"] = sumOfKey(champStats, "5.14", "kda") / 5.0
		champStats["5.14"]["total"]["damage"] = sumOfKey(champStats, "5.14", "damage") / 5.0
		champStats["5.14"]["total"]["killPart"] = sumOfKey(champStats, "5.14", "killPart") / 5.0
		champStats["5.14"]["total"]["damagePerc"] = sumOfKey(champStats, "5.14", "damagePerc") / 5.0
		for itemId in champStats["5.14"]["total"]["items"]:
			champStats["5.14"]["total"]["items"][itemId] = champStats["5.14"]["NA"]["items"][itemId] + champStats["5.14"]["BR"]["items"][itemId] \
			+ champStats["5.14"]["EUW"]["items"][itemId] + champStats["5.14"]["KR"]["items"][itemId] + champStats["5.14"]["EUNE"]["items"][itemId]
		for chId in champStats["5.14"]["total"]["champs"]:
			champStats["5.14"]["total"]["champs"][chId] = champStats["5.14"]["NA"]["champs"][chId] + champStats["5.14"]["BR"]["champs"][chId] \
			+ champStats["5.14"]["EUW"]["champs"][chId] + champStats["5.14"]["KR"]["champs"][chId] + champStats["5.14"]["EUNE"]["champs"][chId]

		with open("jsonFiles/champions/" + champId + ".json", "w") as f:
			f.write(json.dumps(champStats))
			f.close()
		with open("processedChamps.txt", "a") as f:
			f.write(champId + "\n")
			f.close()