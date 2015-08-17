import sqlite3, sys

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Please run with a .db file to create")
		exit()
	db = sqlite3.connect(sys.argv[1])
	cursor = db.cursor()
	cursor.execute("CREATE TABLE players(matchId INTEGER, matchDuration INTEGER, teamId INTEGER, \
				patch TEXT, gameMode TEXT, region TEXT, championId INTEGER, item0 INTEGER, \
				item1 INTEGER, item2 INTEGER, item3 INTEGER, item4 INTEGER, item5 INTEGER, \
				item6 INTEGER, kills INTEGER, deaths INTEGER, assists INTEGER, kda REAL, \
				goldEarned INTEGER, totalDamage INTEGER, magicDamage INTEGER, \
				physDamage INTEGER, avgDamageDiff INTEGER, avgGoldDiff INTEGER, avgKdaDiff REAL, \
				killPart INTEGER, damagePerc INTEGER, goldPerc INTEGER, carried INTEGER)")
	db.commit()
	db.close()