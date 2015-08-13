import urllib2, json, time, sys

# This script takes in a json file of match ids as the first argument and processes each match.
# Processing a match involves making the API request to get match data, generating our own player
# objects and data, and determining which players carried.

def loadChamps():
	champDict = {}
	with open("champData.json") as f:
		for line in f:
			line = line.strip()
			line = line.split("::") # our delimiter
			id = line[0]
			name = line[1]
			champDict[id] = name
	return champDict

def loadItems():
	itemDict = {}
	with open("itemData.json") as f:
		for line in f:
			line = line.strip()
			line = line.split("::") # our delimiter
			id = line[0]
			name = line[1]
			itemDict[id] = name
	return itemDict

itemDict = loadItems()
champDict = loadChamps()

# Appends the given string plus a new line to the file. Useful for populating our json files.
def appendToFile(filename, string):
	with open(filename, "a") as f:
		f.write(string + "\n")
		f.close()

# put api key into file to protect it
def loadAPIKey():
	with open("apiKey.txt") as f:
		for line in f:
			# first line is api key
			return str(line.strip())

# Gets a yes or no from the user. Returns true if yes, false if no.
def verifyInput(index):
	while(True):
		userInput = raw_input("Are you sure index " + str(index) + " carried? [y/n]: ")
		if(len(userInput) < 1):
			continue
		if(userInput[0] == "y" or userInput[0] == "Y"):
			return True
		elif(userInput[0] == "n" or userInput[0] == "N"):
			return False
		else:
			print("Please enter some form of yes or no.")

# Make sure we don't repeat matches by adding processed ones to a text document and returning the set.
def loadProcessedMatches():
	processedMatches = set()
	with open("processedMatches.txt") as f:
		for line in f:
			matchId = line.strip()
			processedMatches.add(matchId)
		f.close()
	return processedMatches

# Given an id, gets the champion's name.
def getChampName(champId):
	if not champId in champDict:
		return "Error"
	else:
		return champDict[champId]

# Given an id, gets the item's name.
def getItemName(itemId):
	if not itemId in itemDict:
		return "Error"
	else:
		return itemDict[itemId]

def generateTrainingData(players, matchId):
	with open("matchStats" + matchId + ".csv", "w") as f:
		f.write("Index,Champion,Kills,Deaths,Assists,KDA,Gold,Damage,avgKdaDiff,avgGoldDiff,avgDamageDiff,killPart,damagePerc,goldPerc")
		f.write("\n")
		for i in range(0, len(players)):
			player = players[i]
			f.write(str(i) + "," + player["championName"] + "," + str(player["kills"]) + "," + str(player["deaths"]) + "," + str(player["assists"]) + "," \
					+ str(player["kda"]) + "," + str(player["goldEarned"]) + "," + str(player["totalDamage"]) + "," \
					+ str(player["avgKdaDiff"]) + "," + str(player["avgGoldDiff"]) + "," + str(player["avgDamageDiff"]) + "," + str(player["killPart"])
					+ "%," + str(player["damagePerc"]) + "%," + str(player["goldPerc"]) + "%")
			f.write("\n")

	while(True):
		index = raw_input("Index of someone who carried (negative number or enter to stop): ")
		if(index == ""):
			break
		try:
			if(int(index) < 0):
				break
		except ValueError:
			print("Invalid index. Please try again.")
			continue	
		index = int(index)
		verified = verifyInput(index)
		if(verified):
			print("Player at index " + str(index) + " marked as a carry.")
			player = players[index]
			player["carried"] = True
		else:
			print("Player at index " + str(index) + " NOT marked as a carry.")		

	for player in players:
		appendToFile("trainingData.json", str(player) + ",") # remove this after model is trained
		if(player["carried"]):
			appendToFile("carryPlayers.json", str(player) + ",")

	#exit() #comment this when ready for real
	appendToFile("processedMatches.txt", matchId)

def processMatch(matchId):
	region = "na"
	matchVersion = "2.2"
	apiKey = loadAPIKey()
	url = "https://na.api.pvp.net/api/lol/" + region + "/v" + matchVersion + "/match/" + matchId + "?api_key=" + apiKey

	# simple API request to get response as plaintext
	try:
		content = urllib2.urlopen(url)
	except urllib2.HTTPError, e:
		if(e.code != 200):
			print("Error in API request for processMatch :(")
			if(content.code == 429): # too many requests
				time.sleep(1) # sleep a second before trying again
				processMatch(matchId)
				return
			else:
				print("Aborting processing of match: " + str(matchId))
				return

	response = str(content.read()) # str() so that it is not unicode
	# convert response to json
	response = json.loads(response)

	region = response["region"]
	gameMode = response["queueType"]
	patch = response["matchVersion"]

	players = [] # our array to populate
	participants = response["participants"]
	totalKills100 = 0
	totalKills200 = 0
	totalDamage100 = 0
	totalDamage200 = 0
	totalGold100 = 0
	totalGold200 = 0
	for participant in participants:
		# initialize with fields that are same for every player
		player = {"region": str(region), "gameMode": str(gameMode), "patch": str(patch), "matchId": str(matchId)}
		player["championId"] = str(participant["championId"])
		stats = participant["stats"]
		player["kills"] = int(stats["kills"])
		player["assists"] = int(stats["assists"])
		player["deaths"] = int(stats["deaths"])
		player["kda"] = round((float(player["kills"]) + float(player["assists"]) / 2.0) / float(player["deaths"]), 2) # our own kda where assists are worth one third of kills
		player["goldEarned"] = int(stats["goldEarned"])
		player["item0"] = str(stats["item0"])
		player["item1"] = str(stats["item1"])
		player["item2"] = str(stats["item2"])
		player["item3"] = str(stats["item3"])
		player["item4"] = str(stats["item4"])
		player["item5"] = str(stats["item5"])
		player["item6"] = str(stats["item6"])
		player["magicDamage"] = int(stats["magicDamageDealtToChampions"])
		player["physDamage"] = int(stats["physicalDamageDealtToChampions"])
		player["totalDamage"] = int(stats["totalDamageDealtToChampions"])
		player["teamId"] = int(participant["teamId"])
		if(player["teamId"] == 100):
			totalKills100 += player["kills"]
			totalGold100 += player["goldEarned"]
			totalDamage100 += player["totalDamage"]
		elif(player["teamId"] == 200):
			totalKills200 += player["kills"]
			totalGold200 += player["goldEarned"]
			totalDamage200 += player["totalDamage"]
		else:
			print("Unknown team id in processMatch: " + str(player["teamId"]))
		player["carried"] = False # will be changed in the machine learning part
		players.append(player)

	for player in players:
		if(player["teamId"] == 100):
			player["killPart"] = int(round(float(player["kills"] + player["assists"]) / totalKills100, 2) * 100)
			player["damagePerc"] = int(round(float(player["totalDamage"]) / totalDamage100, 2) * 100)
			player["goldPerc"] = int(round(float(player["goldEarned"]) / totalGold100, 2) * 100)
		elif(player["teamId"] == 200):
			player["killPart"] = int(round(float(player["kills"] + player["assists"]) / totalKills200, 2) * 100)
			player["damagePerc"] = int(round(float(player["totalDamage"]) / totalDamage200, 2) * 100)
			player["goldPerc"] = int(round(float(player["goldEarned"]) / totalGold200, 2) * 100)


		goldEarned = player["goldEarned"]
		kda = player["kda"]
		damage = player["totalDamage"]
		avgGoldDiff = 0
		avgKdaDiff = 0
		avgDamageDiff = 0
		for otherPlayer in players:
			if(otherPlayer == player):
				continue
			avgGoldDiff += goldEarned - otherPlayer["goldEarned"]
			avgKdaDiff += round(kda - otherPlayer["kda"], 2)
			avgDamageDiff += damage - otherPlayer["totalDamage"]
		avgGoldDiff /= len(players) - 1 # minus 1 because didn't compare to self
		avgKdaDiff /= len(players) - 1
		avgDamageDiff /= len(players) - 1
		player["avgGoldDiff"] = avgGoldDiff
		player["avgKdaDiff"] = round(avgKdaDiff, 2)
		player["avgDamageDiff"] = avgDamageDiff

		player["championName"] = getChampName(player["championId"])
		for i in range(0, 7):
			player["itemName" + str(i)] = getItemName(player["item" + str(i)])
		appendToFile("trainingData.json", str(player) + ",")
	generateTrainingData(players, matchId)

if __name__ == "__main__":
	processedMatches = loadProcessedMatches()
	print("You have trained for " + str(len(processedMatches)) + " matches already! :)")

	with open(sys.argv[1]) as f:
		for line in f:
			# skip over non match ids
			if(not line[0].isdigit()):
				continue
			line = line.strip() # remove \r\n
			matchId = line.replace(",", "") # remove comma
			if(not matchId in processedMatches):
				print("Advancing to match: " + matchId)
				processMatch(matchId)
			else:
				print("Skipping over match: " + matchId + " because it was already processed.")
