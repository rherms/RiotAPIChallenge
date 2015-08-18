import json, sys, sqlite3, copy

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

if __name__ == '__main__':
	if(len(sys.argv) < 2):
		print("Please run with a champion id to generate data for.")


	itemDict = loadDict("itemData.txt")
	itemDict = fixItems(itemDict)
	champDict = loadDict("champData.txt")

	champId = sys.argv[1]

	databases = [["5.11", "NA", "Databases/5.11/Ranked/NA.db"], ["5.11", "BR", "Databases/5.11/Ranked/BR.db"], ["5.11", "EUNE", "Databases/5.11/Ranked/EUNE.db"]]

	defaultItems = {}
	for itemId in itemDict:
		defaultItems[int(itemId)] = 0

	defaultChamps = {}
	for chId in champDict:
		defaultChamps[int(chId)] = 0

	defaultStats = {
		"gamesPlayed": 0,
		"gamesCarried": 0,
		"carried": {
			"items": copy.deepcopy(defaultItems),
			"champs": copy.deepcopy(defaultChamps),
			"kills": 0,
			"deaths": 0,
			"assists": 0,
			"kda": 0,
			"damage": 0,
			"killPart": 0,
			"damagePerc": 0
		},
		"notCarried": {
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
	}

	defaultObj = {
		"total": copy.deepcopy(defaultStats),
		"BR": copy.deepcopy(defaultStats),
		"EUNE": copy.deepcopy(defaultStats),
		"EUW": copy.deepcopy(defaultStats),
		"NA": copy.deepcopy(defaultStats)
	}

	champStats = {
		"5.11": copy.deepcopy(defaultObj),
		"5.14": copy.deepcopy(defaultObj)	
	}


	for dbInfo in databases:
		# Just chose this order to have all variables conveniently
		patch = dbInfo[0]
		region = dbInfo[1]
		filename = dbInfo[2]
		db = sqlite3.connect(filename)
		cursor = db.cursor()
		cursor.execute("SELECT count(*) from players where championId=" + champId)
		rows = cursor.fetchall()
		count = rows[0][0] # first row, tuple of just one value
		champStats[patch][region]["gamesPlayed"] = count
		champStats[patch]["total"]["gamesPlayed"] += count

		cursor.execute("SELECT count(*) from players where carried=1 and championId=" + champId)
		rows = cursor.fetchall()
		count = rows[0][0] # first row, tuple of just one value
		champStats[patch][region]["gamesCarried"] = count
		#champStats[patch]["total"]["gamesCarried"] += count  CAN DO ALL TOTALING AFTER BY LOOPING OVER REGIONS

		cursor.execute("SELECT item0, item1, item2, item3, item4, item5, item6, kills, deaths, assists, totalDamage, killPart, damagePerc from players where carried=1 and championId=" + champId)
		rows = cursor.fetchall()
		for row in rows:
			items = row[:7]
			for itemId in items:
				if(itemId == 0):
					continue
				if itemId in champStats[patch][region]["carried"]["items"]:
					champStats[patch][region]["carried"]["items"][itemId] += 1

			kills = row[7]
			deaths = row[8]
			assists = row[9]
			damage = row[10]
			killPart = row[11]
			damagePerc = row[12]

			champStats[patch][region]["carried"]["kills"] += kills
			champStats[patch][region]["carried"]["deaths"] += deaths
			champStats[patch][region]["carried"]["assists"] += assists
			champStats[patch][region]["carried"]["damage"] += damage
			champStats[patch][region]["carried"]["killPart"] += killPart
			champStats[patch][region]["carried"]["damagePerc"] += damagePerc
		if(champStats[patch][region]["carried"]["deaths"] == 0):
			champStats[patch][region]["carried"]["kda"] = 100
		else:
			champStats[patch][region]["carried"]["kda"] = float(champStats[patch][region]["carried"]["kills"] + champStats[patch][region]["carried"]["assists"]) / champStats[patch][region]["carried"]["deaths"]
		gamesCarried = float(champStats[patch][region]["gamesCarried"])
		if(champStats[patch][region]["gamesCarried"] > 0):
			champStats[patch][region]["carried"]["kills"] /= gamesCarried
			champStats[patch][region]["carried"]["deaths"] /= gamesCarried
			champStats[patch][region]["carried"]["assists"] /= gamesCarried
			champStats[patch][region]["carried"]["damage"] /= gamesCarried
			champStats[patch][region]["carried"]["killPart"] /= gamesCarried
			champStats[patch][region]["carried"]["damagePerc"] /= gamesCarried

		cursor.execute("SELECT matchId, teamId from players where carried=1 and championId=" + champId)
		rows = cursor.fetchall()
		for row in rows:
			matchId = row[0]
			teamId = row[1]
			cursor.execute("SELECT championId from players where matchId=" + str(matchId) + " and teamId=" + str(teamId))
			newRows = cursor.fetchall()
			for newRow in newRows:
				championId = newRow[0]
				champStats[patch][region]["carried"]["champs"][championId] += 1

		# not going to populate "not carried" fields for now in the interest of time
		# don't forget to do kda at the end

		db.close()
		
	###################################################
	# populate the total fields of 5.11 and 5.14 here #
	###################################################

	with open(champId + ".json", "w") as f:
		f.write(json.dumps(champStats))