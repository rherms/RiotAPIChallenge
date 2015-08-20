import json, sys, sqlite3, copy, urllib2

def convert(itemId):
	itemId = int(itemId)
	if(itemId <= 3284 and itemId >= 3280):
		return "3009"
	if(itemId <= 3279 and itemId >= 3275):
		return "3158"
	if(itemId <= 3254 and itemId >= 3250):
		return "3006"
	if(itemId <= 3259 and itemId >= 3255):
		return "3020"
	if(itemId <= 3264 and itemId >= 3260):
		return "3047"
	if(itemId <= 3269 and itemId >= 3265):
		return "3111"
	if(itemId <= 3274 and itemId >= 3270):
		return "3117"
	return itemId	
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

def sumOfItems(itemStats, patch, itemId):
	return itemStats[patch]["NA"][key] + itemStats[patch]["BR"][key] + itemStats[patch]["EUNE"][key] + itemStats[patch]["EUW"][key] + itemStats[patch]["KR"][key]

def sumOfKey(itemStats, patch, key):
	return itemStats[patch]["NA"][key] + itemStats[patch]["BR"][key] + itemStats[patch]["EUNE"][key] + itemStats[patch]["EUW"][key] + itemStats[patch]["KR"][key]

if __name__ == '__main__':
	#if(len(sys.argv) < 2):
	#	print("Please run with a champion id to generate data for.")
	processedItems = set()
	with open("processedItems.txt") as f:
		for line in f:
			line = line.strip()
			processedItems.add(line)
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
		"gamesBuilt": 0,
		"gamesCarried": 0,
		"items": copy.deepcopy(defaultItems),
		"champs": copy.deepcopy(defaultChamps),
	}

	defaultObj = {
		"total": copy.deepcopy(defaultStats),
		"BR": copy.deepcopy(defaultStats),
		"EUNE": copy.deepcopy(defaultStats),
		"EUW": copy.deepcopy(defaultStats),
		"NA": copy.deepcopy(defaultStats),
		"KR": copy.deepcopy(defaultStats)
	}
	apiKey = loadAPIKey()
	for itemId in itemDict: 
		if(itemId in processedItems):
			print("Item " + itemId + " already processed. Skipping.")
			continue
		itemStats = {
			"description": "",
			"name": "",
			"5.11": copy.deepcopy(defaultObj),
			"5.14": copy.deepcopy(defaultObj)	
		}
		print("Advancing to item " + itemId)

		#url = "https://na.api.pvp.net/api/lol/static-data/na/v1.2/item/" + itemId + "?api_key=" + apiKey
		url = "https://na.api.pvp.net/api/lol/static-data/na/v1.2/item/" + convert(itemId) + "?api_key=" + apiKey
		# simple API request to get response as plaintext
		try:
			content = urllib2.urlopen(url)
		except urllib2.HTTPError, e:
			if(e.code != 200):
				print("Error in API request for item " + itemId + " :(    " + str(e.code))
				continue
		response = str(content.read()) # str() so that it is not unicode
		# convert response to json
		response = json.loads(response)
		itemStats["description"] = response["description"]
		itemStats["name"] = response["name"]

		for dbInfo in databases:
			# Just chose this order to have all variables conveniently
			patch = dbInfo[0]
			region = dbInfo[1]
			filename = dbInfo[2]
			print("Advancing to database: " + filename)
			db = sqlite3.connect(filename)
			cursor = db.cursor()
			cursor.execute("SELECT count(*) from players where item0=" + itemId + " or item1=" + itemId + " or item2=" + itemId + " or item3=" + itemId + " or item4=" + itemId + " or item5=" + itemId + " or item6=" + itemId)
			rows = cursor.fetchall()
			count = rows[0][0] # first row, tuple of just one value
			itemStats[patch][region]["gamesBuilt"] = count

			cursor.execute("SELECT count(*) from players where carried=1 and (item0=" + itemId + " or item1=" + itemId + " or item2=" + itemId + " or item3=" + itemId + " or item4=" + itemId + " or item5=" + itemId + " or item6=" + itemId + ")")
			rows = cursor.fetchall()
			count = rows[0][0] # first row, tuple of just one value
			itemStats[patch][region]["gamesCarried"] = count

			cursor.execute("SELECT item0, item1, item2, item3, item4, item5, item6, championId from players where carried=1 and (item0=" + itemId + " or item1=" + itemId + " or item2=" + itemId + " or item3=" + itemId + " or item4=" + itemId + " or item5=" + itemId + " or item6=" + itemId + ")")
			rows = cursor.fetchall()
			for row in rows:
				items = row[:7]
				for itId in items:
					if(itId == 0):
						continue
					if itId in itemStats[patch][region]["items"]:
						itemStats[patch][region]["items"][itId] += 1

				championId = row[7]
				itemStats[patch][region]["champs"][championId] += 1

			db.close()
			
		###################################################
		# populate the total fields of 5.11 and 5.14 here #
		###################################################
		itemStats["5.11"]["total"]["gamesBuilt"] = sumOfKey(itemStats, "5.11", "gamesBuilt")
		itemStats["5.11"]["total"]["gamesCarried"] = sumOfKey(itemStats, "5.11", "gamesCarried")
		
		for itId in itemStats["5.11"]["total"]["items"]:
			itemStats["5.11"]["total"]["items"][itId] = itemStats["5.11"]["NA"]["items"][itId] + itemStats["5.11"]["BR"]["items"][itId] \
			+ itemStats["5.11"]["EUW"]["items"][itId] + itemStats["5.11"]["KR"]["items"][itId] + itemStats["5.11"]["EUNE"]["items"][itId]
		for chId in itemStats["5.11"]["total"]["champs"]:
			itemStats["5.11"]["total"]["champs"][chId] = itemStats["5.11"]["NA"]["champs"][chId] + itemStats["5.11"]["BR"]["champs"][chId] \
			+ itemStats["5.11"]["EUW"]["champs"][chId] + itemStats["5.11"]["KR"]["champs"][chId] + itemStats["5.11"]["EUNE"]["champs"][chId]

		itemStats["5.14"]["total"]["gamesBuilt"] = sumOfKey(itemStats, "5.14", "gamesBuilt")
		itemStats["5.14"]["total"]["gamesCarried"] = sumOfKey(itemStats, "5.14", "gamesCarried")
		
		for itId in itemStats["5.14"]["total"]["items"]:
			itemStats["5.14"]["total"]["items"][itId] = itemStats["5.14"]["NA"]["items"][itId] + itemStats["5.14"]["BR"]["items"][itId] \
			+ itemStats["5.14"]["EUW"]["items"][itId] + itemStats["5.14"]["KR"]["items"][itId] + itemStats["5.14"]["EUNE"]["items"][itId]
		for chId in itemStats["5.14"]["total"]["champs"]:
			itemStats["5.14"]["total"]["champs"][chId] = itemStats["5.14"]["NA"]["champs"][chId] + itemStats["5.14"]["BR"]["champs"][chId] \
			+ itemStats["5.14"]["EUW"]["champs"][chId] + itemStats["5.14"]["KR"]["champs"][chId] + itemStats["5.14"]["EUNE"]["champs"][chId]

		with open("jsonFiles/items/" + itemId + ".json", "w") as f:
			f.write(json.dumps(itemStats))
		with open("processedItems.txt", "a") as f:
			f.write(itemId + "\n")
			f.close()