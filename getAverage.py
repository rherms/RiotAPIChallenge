import json, os, heapq

counter = 0
total511 = 0
total514 = 0
path = "C:/Users/rlher_000/Documents/RiotAPIChallenge/jsonFiles/items" #champions"
for jsonFile in os.listdir(path):
	with open(path + "/" + jsonFile) as f:
		for line in f:
			line = line.strip()
			data = json.loads(line)
			total511 += data["5.11"]["total"]["gamesBuilt"]
			total514 += data["5.14"]["total"]["gamesBuilt"]
		f.close()
	counter += 1

avg511 = total511 / float(counter)
avg514 = total514 / float(counter)
print("5.11 Champs: " + str(avg511))
print("5.14 Champs: " + str(avg514))


