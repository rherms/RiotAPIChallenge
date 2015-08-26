import json, os, heapq

def getTop10(champs):
	keys = []
	for champ in champs:
		for key in champ:
			keys.append(key)
	keys = heapq.nlargest(30, keys)
	top10 = []
	for champ in champs:
		for key in champ:
			if key in keys:
				top10.append(champ)

	return top10

top511Champs = []
top514Champs = []
path = "C:/Users/rlher_000/Documents/RiotAPIChallenge/jsonFiles/items"
for jsonFile in os.listdir(path):
	with open(path + "/" + jsonFile) as f:
		for line in f:
			line = line.strip()
			data = json.loads(line)
			if(data["5.11"]["total"]["gamesBuilt"] == 0):#< 9787 / 2):
				carryRate511 = 0
			else:
				carryRate511 = float(data["5.11"]["total"]["gamesCarried"]) / float(data["5.11"]["total"]["gamesBuilt"])
				#carryRate511 = int(data["5.11"]["total"]["gamesCarried"])
			if(data["5.14"]["total"]["gamesBuilt"] ==0):#< 9787 / 2):
				carryRate514 = 0
			else:
				carryRate514 = float(data["5.14"]["total"]["gamesCarried"]) / float(data["5.14"]["total"]["gamesBuilt"])
				#carryRate514 = int(data["5.14"]["total"]["gamesCarried"])
			name = data["name"]
			newObj1 = {carryRate511: name}
			newObj2 = {carryRate514: name}
			top511Champs.append(newObj1)
			top514Champs.append(newObj2)
		f.close()

top10Champs511 = getTop10(top511Champs)
top10Champs514 = getTop10(top514Champs)

print(top10Champs511)
print(top10Champs514)


