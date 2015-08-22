from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
import json, os
# Create your views here.
def index(request):
	return render(request, "index.html")

def champions(request, champId=""):
	data = {}
	module_dir = os.path.dirname(__file__)  # get current directory
	file_path = os.path.join(module_dir, "jsonFiles/champions/" + champId + ".json")
	
	champDict = {}
	with open(os.path.join(module_dir, "champData.txt")) as f:
		for line in f:
			line = line.strip()
			line = line.split("::")
			key = line[0]
			val = line[1]
			champDict[key] = val
		f.close()
	itemDict = {}
	with open(os.path.join(module_dir, "itemData.txt")) as f:
		for line in f:
			line = line.strip()
			line = line.split("::")
			key = line[0]
			val = line[1]
			itemDict[key] = val
		f.close()

	if(not champId in champDict):
		return HttpResponseNotFound("<h1> Sorry, page not found :( </h1>")

	with open(file_path) as f:
		for line in f:
			data = line.strip()
		f.close()

	return render(request, "champion.html", {"data": str(data), "itemDict": json.dumps(itemDict), "champDict": json.dumps(champDict), "champId": champId})

def items(request, itemId=""):
	data = {}
	module_dir = os.path.dirname(__file__)  # get current directory
	file_path = os.path.join(module_dir, "jsonFiles/items/" + itemId + ".json")
	
	champDict = {}
	with open(os.path.join(module_dir, "champData.txt")) as f:
		for line in f:
			line = line.strip()
			line = line.split("::")
			key = line[0]
			val = line[1]
			champDict[key] = val
		f.close()
	itemDict = {}
	with open(os.path.join(module_dir, "itemData.txt")) as f:
		for line in f:
			line = line.strip()
			line = line.split("::")
			key = line[0]
			val = line[1]
			itemDict[key] = val
		f.close()

	if(not itemId in itemDict):
		return HttpResponseNotFound("<h1> Sorry, page not found :( </h1>")
			
	with open(file_path) as f:
		for line in f:
			data = line.strip()
		f.close()

	return render(request, "item.html", {"data": str(data), "itemDict": json.dumps(itemDict), "champDict": json.dumps(champDict), "itemId": itemId})
