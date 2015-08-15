import json
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib

def normalize(x, maxX, minX):
	return float(x - minX) / (maxX - minX)

if __name__ == "__main__":
	model = KNeighborsClassifier()

	# max and mins for normalizing data later
	maxKills = 0
	minKills = 999999 # some big number
	maxDeaths = 0
	minDeaths = 999999
	maxAssists = 0
	minAssists = 999999
	maxKda = 0
	minKda = 999999
	maxGold = 0
	minGold = 999999
	maxDam = 0
	minDam = 999999
	maxKdaDiff = 0
	minKdaDiff = 999999
	maxGoldDiff = 0
	minGoldDiff = 999999
	maxDamDiff = 0
	minDamDiff = 999999
	maxKillPart = 0
	minKillPart = 999999
	maxDamPerc = 0
	minDamPerc = 999999

	X = []
	Y = []

	with open("trainingData.json") as f:
		for line in f:
			obj = json.loads(line.strip())
			kills = obj["kills"]
			deaths = obj["deaths"]
			assists = obj["assists"]
			kda = obj["kda"]
			gold = obj["goldEarned"]
			damage = obj["totalDamage"]
			kdaDiff = obj["avgKdaDiff"]
			goldDiff = obj["avgGoldDiff"]
			damDiff = obj["avgDamageDiff"]
			killPart = obj["killPart"]
			damPerc = obj["damagePerc"]

			# store data as an array for k nearest neighbors
			nextX = [kills, deaths, assists, kda, gold, damage, kdaDiff, goldDiff, damDiff, killPart, damPerc]
			X.append(nextX)

			# 1 means carried, 0 means didn't carry
			if(obj["carried"]):
				Y.append(1)
			else:
				Y.append(0)

			# update all max/min variables
			if kills > maxKills:
				maxKills = kills
			if kills < minKills:
				minKills = kills
			if deaths > maxDeaths:
				maxDeaths = deaths
			if deaths < minDeaths:
				minDeaths = deaths
			if assists > maxAssists:
				maxAssists = assists
			if assists < minAssists:
				minAssists = assists
			if kda > maxKda:
				maxKda = kda
			if kda < minKda:
				minKda = kda
			if gold > maxGold:
				maxGold = gold
			if gold < minGold:
				minGold = gold
			if damage > maxDam:
				maxDam = damage
			if damage < minDam:
				minDam = damage
			if kdaDiff > maxKdaDiff:
				maxKdaDiff = kdaDiff
			if kdaDiff < minKdaDiff:
				minKdaDiff = kdaDiff
			if goldDiff > maxGoldDiff:
				maxGoldDiff = goldDiff
			if goldDiff < minGoldDiff:
				minGoldDiff = goldDiff
			if damDiff > maxDamDiff:
				maxDamDiff = damDiff
			if damDiff < minDamDiff:
				minDamDiff = damDiff
			if killPart > maxKillPart:
				maxKillPart = killPart
			if killPart < minKillPart:
				minKillPart = killPart
			if damPerc > maxDamPerc:
				maxDamPerc = damPerc
			if damPerc < minDamPerc:
				minDamPerc = damPerc	
		f.close()

	with open("normData.txt", "w") as f:
		f.write("maxKills::" + str(maxKills) + "\n")
		f.write("minKills::" + str(minKills) + "\n")		
		f.write("maxDeaths::" + str(maxDeaths) + "\n")
		f.write("minDeaths::" + str(minDeaths) + "\n")	
		f.write("maxAssists::" + str(maxAssists) + "\n")
		f.write("minAssists::" + str(minAssists) + "\n")	
		f.write("maxKda::" + str(maxKda) + "\n")
		f.write("minKda::" + str(minKda) + "\n")	
		f.write("maxGold::" + str(maxGold) + "\n")
		f.write("minGold::" + str(minGold) + "\n")	
		f.write("maxDam::" + str(maxDam) + "\n")
		f.write("minDam::" + str(minDam) + "\n")	
		f.write("maxKdaDiff::" + str(maxKdaDiff) + "\n")
		f.write("minKdaDiff::" + str(minKdaDiff) + "\n")	
		f.write("maxGoldDiff::" + str(maxGoldDiff) + "\n")
		f.write("minGoldDiff::" + str(minGoldDiff) + "\n")	
		f.write("maxDamDiff::" + str(maxDamDiff) + "\n")
		f.write("minDamDiff::" + str(minDamDiff) + "\n")	
		f.write("maxKillPart::" + str(maxKillPart) + "\n")
		f.write("minKillPart::" + str(minKillPart) + "\n")	
		f.write("maxDamPerc::" + str(maxDamPerc) + "\n")
		f.write("minDamPerc::" + str(minDamPerc) + "\n")	

	for i in range(0, len(X)):
		# array is in following format: kills, deaths, assists, kda, gold, damage, kdaDiff, goldDiff, damageDiff, killPart, damagePerc
		dataPoint = X[i]

		# normalize each piece of data and update X
		dataPoint[0] = normalize(dataPoint[0], maxKills, minKills)
		dataPoint[1] = normalize(dataPoint[1], maxDeaths, minDeaths)
		dataPoint[2] = normalize(dataPoint[2], maxAssists, minAssists)
		dataPoint[3] = normalize(dataPoint[3], maxKda, minKda)
		dataPoint[4] = normalize(dataPoint[4], maxGold, minGold)
		dataPoint[5] = normalize(dataPoint[5], maxDam, minDam)
		dataPoint[6] = normalize(dataPoint[6], maxKdaDiff, minKdaDiff)
		dataPoint[7] = normalize(dataPoint[7], maxGoldDiff, minGoldDiff)
		dataPoint[8] = normalize(dataPoint[8], maxDamDiff, minDamDiff)
		dataPoint[9] = normalize(dataPoint[9], maxKillPart, minKillPart)
		dataPoint[10] = normalize(dataPoint[10], maxDamPerc, minDamPerc)

		X[i] = dataPoint

	model.fit(X, Y)
	joblib.dump(model, "knnModel.pkl")
