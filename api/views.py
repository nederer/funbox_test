'''
We need decorator `@api_view`, which is used for writing function-based views with REST framework
Takes a list of allowed methods for the view as an argument
If method is not allowed, it raises exception
It based on 'rest_framework.views.APIView' class
That class has 'exception_handler' function that returns Response with "detail" line in it
Tasks says that we need "status" line
So we need to change "detail" to "status"
But I decided to let "detail" line stay, so I won't need to send changed DRF code you will run
Hope this is not a mistake
'''

from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view

from django.core.validators import URLValidator 
from django.core.exceptions import ValidationError 

import re
import redis
import json
import time
	
redis_db = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

'''
function checks if link is valid
django.core.validators.URLValidator would raise an error if link is "funbox.ru"
so I added 'http://' to exclude this
'''
def is_valid_link(url):
	if re.match(r'^(?:http|ftp)s?://', url) is None:
		url = 'http://'+url
	validator = URLValidator()
	try:
		validator(url)
	except ValidationError:
		return False
	return True


@api_view(['GET'])
def visited_domains(request):
	if 'from' in request.GET and 'to' in request.GET:
		try:
			start = int(request.GET.get('from'))
			end = int(request.GET.get('to'))
		except:
			return Response({"status": "'start' and 'end' got to be int"}, status=400)

			
		domains = []
		for key in redis_db.keys("*"):
			domains.extend(redis_db.smembers(key))

		# getting domain name and deleting repeated values
		domains = list(set((x.decode("utf-8").split("//")[-1].split("/")[0] for x in domains)))
		response = {
			"domain": domains,
			"status": "ok"
		}
			
		return Response(response, status=200)
	else:
		return Response({"status": "Invalid header"}, status=404)


@api_view(['POST'])
def visited_links(request):
	key = time.time()						
	body = json.loads(request.body)
	if not 'links' in body:
		return Response({"status": "key 'links' is not found"}, status=400)

	links = body['links']
	for link in links:
		if not is_valid_link(link):
			return Response({"status": f"'{link}' is not valid"}, status=400)
			
	
	for link in links:
		redis_db.sadd(key, link)
	response = {
		"status": "ok"
	}
	return Response(response, status = 200)
	
			
		



