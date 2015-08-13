import urllib2, json

# put api key into file to protect it
def loadAPIKey():
	with open("apiKey.txt") as f:
		for line in f:
			# first line is api key
			return str(line.strip())

# Appends the given string plus a new line to the file. Useful for populating our json files.
def appendToFile(filename, string):
	with open(filename, "a") as f:
		f.write(string + "\n")
		f.close()

def populateChampions():
	staticVersion = "1.2"
	region = "na"
	apiKey = loadAPIKey()
	url = "https://na.api.pvp.net/api/lol/static-data/na/v" + staticVersion + "/champion?api_key=" + apiKey;
	try:
		content = urllib2.urlopen(url)
	except urllib2.HTTPError, e:
		if(e.code != 200):
			print("Error in API request for populateChampions :(")
			if(e.code == 429): # too many requests
				time.sleep(1) # sleep a second before trying again
				populateChampions()
				return
			else:
				print("Aborting attempt...")
				return

	response = str(content.read()) # str() so that it is not unicode
	# convert response to json
	response = json.loads(response)
	champData = response["data"]
	for champKey in champData:
		champ = champData[champKey]
		champId = champ["id"]
		name = champ["name"]
		appendToFile("champData.json", str(champId) + "::" + str(name)) # "::"" is our delimiter

def populateItems():
	staticVersion = "1.2"
	region = "na"
	apiKey = loadAPIKey()
	url = "https://na.api.pvp.net/api/lol/static-data/na/v" + staticVersion + "/item?api_key=" + apiKey;
	try:
		content = urllib2.urlopen(url)
	except urllib2.HTTPError, e:
		if(e.code != 200):
			print("Error in API request for populateItems :(")
			if(e.code == 429): # too many requests
				time.sleep(1) # sleep a second before trying again
				populateItems()
				return
			else:
				print("Aborting attempt...")
				return

	response = str(content.read()) # str() so that it is not unicode
	# convert response to json
	response = json.loads(response)
	itemData = response["data"]
	for itemKey in itemData:
		item = itemData[itemKey]
		itemId = item["id"]
		name = item["name"]
		appendToFile("itemData.json", str(itemId) + "::" + str(name)) # "::"" is our delimiter

if __name__ == "__main__":
	populateChampions()
	populateItems()