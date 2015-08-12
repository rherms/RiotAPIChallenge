import urllib2, json

if __name__ == "__main__":

	matchIds = []
	region = "na"
	matchVersion = "2.2"
	apiKey = "981207c1-b746-4fd2-8963-1040c3bfe7a5"

	with open("AP_ITEM_DATASET/5.11/RANKED_SOLO/NA.json") as f:
		for line in f:
			# skip over non match ids
			if(not line[0].isdigit()):
				continue
			line = line.strip() # remove \r\n
			line = line.replace(",", "") # remove comma
			matchIds.append(line)

	id = matchIds[0]
	url = "https://na.api.pvp.net/api/lol/" + region + "/v" + matchVersion + "/match/" + id + "?api_key=" + apiKey
	print(url)
	# simple API request to get response as plaintext
	content = urllib2.urlopen(url)
	
	if(content.code != 200):
		print("Error in API request. Wait before trying again.")
	response = str(content.read()) # str() so that it is not unicode
	# convert response to json
	response = json.loads(response)

	region = response["region"]
	gameMode = response["queueType"]
	patch = response["matchVersion"]

	players = [] # our array to populate
	participants = response["participants"]
	for participant in participants:
		# initialize with fields that are same for every player
		player = {"region": region, "gameMode": gameMode, "patch": patch}
		player["championId"] = participant["championId"]
		stats = participant["stats"]
		player["kills"] = stats["kills"]
		player["assists"] = stats["assists"]
		player["deaths"] = stats["deaths"]
		player["kda"] = float(player["kills"]) + float(player["assists"]) / 3.0 / float(player["deaths"]) # our own kda where assists are worth one third of kills
		player["goldEarned"] = int(stats["goldEarned"])
		player["item0"] = stats["item0"]
		player["item1"] = stats["item1"]
		player["item2"] = stats["item2"]
		player["item3"] = stats["item3"]
		player["item4"] = stats["item4"]
		player["item5"] = stats["item5"]
		player["item6"] = stats["item6"]
		player["magicDamage"] = int(stats["magicDamageDealtToChampions"])
		player["physDamage"] = int(stats["physicalDamageDealtToChampions"])
		player["totalDamage"] = int(stats["totalDamageDealtToChampions"])
		players.append(player)

	for player in players:
		goldEarned = player["goldEarned"]
		kda = player["kda"]
		damage = player["totalDamage"]
		counter = 1 # for incrementing keys
		for otherPlayer in players:
			if(otherPlayer == player):
				continue
			player["goldDiff" + str(counter)] = goldEarned - otherPlayer["goldEarned"]
			player["kdaDiff" + str(counter)] = kda - otherPlayer["kda"]
			player["damageDiff" + str(counter)] = damage - otherPlayer["totalDamage"]
			counter += 1
		#player["championName"] = getChampName(player["championId"])
		#for i in range(0, 7):
		#	player["itemName" + str(i)] = getItemName(player["item" + str(i)])
		print(player)

	#print(response)