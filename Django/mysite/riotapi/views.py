from django.shortcuts import render
from django.http import HttpResponse
import json, os
# Create your views here.
def index(request):
	return HttpResponse("Hello World!")

def champions(request, champName=""):
	data = {}
	# convert name to id
	champId = "67"
	module_dir = os.path.dirname(__file__)  # get current directory
	file_path = os.path.join(module_dir, "jsonFiles/" + champId + ".json")
	with open(file_path) as f:
		for line in f:
			data = line.strip()
		f.close()
	return render(request, "champions.html", {"data": str(data)})

def items(request, itemName=""):
	itemId = "0"
	return HttpResponse("Item: " + itemId)
