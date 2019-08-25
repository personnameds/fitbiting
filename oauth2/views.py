from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from fitbiters.models import Fitbiter
from fitdata.models import FitData
from django.conf import settings
from django.db import IntegrityError
from django.urls import reverse

import requests #need to install this library
from datetime import datetime
import base64
import urllib
import json

import os

def GetFitbitData(fitbiter):
	activity_data=GetDataUsingAccessToken(fitbiter) 
	return activity_data
    
def GetDataUsingAccessToken(fitbiter):

	#Get last_sync
	FitbitDeviceURL='https://api.fitbit.com/1/user/'+fitbiter.fitbit_id+'/devices.json'
	
	devicereq=urllib.request.Request(FitbitDeviceURL)
	devicereq.add_header('Authorization', 'Bearer ' + fitbiter.access_token)
	
	deviceresponse=urllib.request.urlopen(devicereq)
	deviceFullResponse=deviceresponse.read()
	deviceResponseJSON = json.loads(deviceFullResponse)
	
	device_data=deviceResponseJSON
	
	#Updates last sync
	#Not sure what will happen if more than one device
	for d in device_data:
		last_sync=d['lastSyncTime']
		formatted_last_sync=datetime.strptime(last_sync, '%Y-%m-%dT%H:%M:%S.%f')
		fitbiter.last_sync=formatted_last_sync
		fitbiter.save()
	
	last_date=formatted_last_sync.strftime("%Y-%m-%d")

#	last_date=FitData.objects.filter(fitbiter=fitbiter).latest('date').date
	FitData.objects.filter(fitbiter=fitbiter, date=last_date).delete()
#	last_date=last_date.strftime("%Y-%m-%d")
	
	FitbitURL='https://api.fitbit.com/1/user/'+fitbiter.fitbit_id+'/activities/distance/date/'+last_date+'/today.json'
    
	req=urllib.request.Request(FitbitURL)
	
	req.add_header('Authorization', 'Bearer ' + fitbiter.access_token)
	
	try:
		response=urllib.request.urlopen(req)
		
		FullResponse=response.read()
		
		ResponseJSON = json.loads(FullResponse)

		return ResponseJSON
	
	except urllib.request.URLError as e:

		HTTPErrorMessage=str(e.read())
		
		##If Access token Expired
		if (e.code==401) and (HTTPErrorMessage.find("Access token expired") > 0):
			GetNewAccessandRefreshToken(fitbiter)
	
		## Some other error
		else:
			print(e.code)
			print(e.read())
			return False


def GetNewAccessandRefreshToken(fitbiter):
	##Use Refresh token to get new  access token
	BodyText={'refresh_token': fitbiter.refresh_token,
			  'grant_type':'refresh_token',
			  'expires_in':2592000,
			  }
	BodyURLEncoded=urllib.parse.urlencode(BodyText).encode('utf-8')
	
	req=urllib.request.Request(token_url,BodyURLEncoded)

	base64string=str(client_id + ':' + client_secret)
	base64string=bytes(base64string, 'utf-8')

	base64string=base64.b64encode(base64string)
	base64string=base64string.decode('utf-8')
	autho='Basic ' + base64string

	req.add_header('Authorization', autho)
	req.add_header('Content-Type', 'application/x-www-form-urlencoded')

	try:
		response=urllib.request.urlopen(req)
		FullResponse=response.read()

	except urllib.request.URLError as e:
		print(e.code)
		print(e.read())

	## Access and Refresh Token Received
	## Saving tokens to model
	ResponseJSON = json.loads(FullResponse)

	fitbiter.access_token = str(ResponseJSON['access_token'])
	fitbiter.refresh_token = str(ResponseJSON['refresh_token'])
	fitbiter.save()

	GetDataUsingAccessToken(fitbiter)

##New User
def Oauth2View(request):
	
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	
	CLIENT_DIRECTORY=os.path.join(BASE_DIR,'fitbiting')+'/REDIRECT_URI'
	with open(CLIENT_DIRECTORY) as f:
		REDIRECT_URI = f.read().strip()
	
	redirect_uri=REDIRECT_URI
		
	redirect_uri=urllib.parse.quote(redirect_uri, safe='')
	authorize_url='https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=22CVHF&redirect_uri='+redirect_uri+'&scope=activity%20settings&expires_in=604800'
	return HttpResponseRedirect(authorize_url)

def Oauth2CallBackView(request):
	
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


	CLIENT_DIRECTORY=os.path.join(BASE_DIR,'fitbiting')+'/CLIENT_ID'
	with open(CLIENT_DIRECTORY) as f:
		CLIENT_ID = f.read().strip()

	CLIENT_DIRECTORY=os.path.join(BASE_DIR,'fitbiting')+'/CLIENT_SECRET'
	with open(CLIENT_DIRECTORY) as f:
		CLIENT_SECRET = f.read().strip()

	CLIENT_DIRECTORY=os.path.join(BASE_DIR,'fitbiting')+'/REDIRECT_URI'
	with open(CLIENT_DIRECTORY) as f:
		REDIRECT_URI = f.read().strip()

	client_id=CLIENT_ID
	client_secret=CLIENT_SECRET
	redirect_uri=REDIRECT_URI



	token_url='https://api.fitbit.com/oauth2/token'
	
	code=request.GET.get('code')
	
	##To Get Access and Refresh Token
	BodyText={'code':code,
			  'redirect_uri':redirect_uri,
			  'client_id': client_id,
			  'grant_type':'authorization_code',
			  'expires_in':2592000,
			  }
	BodyURLEncoded=urllib.parse.urlencode(BodyText).encode('utf-8')
	
	req=urllib.request.Request(token_url,BodyURLEncoded)
	
	base64string=str(client_id + ':' + client_secret)
	base64string=bytes(base64string, 'utf-8')
	
	base64string=base64.b64encode(base64string)
	base64string=base64string.decode('utf-8')
	autho='Basic ' + base64string
	
	req.add_header('Authorization', autho)
	req.add_header('Content-Type', 'application/x-www-form-urlencoded')
	
	try:
		response=urllib.request.urlopen(req)
		FullResponse=response.read()
		
		print(FullResponse)
		
	except urllib.request.URLError as e:
		print(e.code)
		print(e.read())
		
	## Access and Refresh Token Received
	## Saving tokens to model
	ResponseJSON = json.loads(FullResponse)

	fitbiter=Fitbiter(fitbit_id=str(ResponseJSON['user_id']),
					  access_token=str(ResponseJSON['access_token']),
					  refresh_token=str(ResponseJSON['refresh_token']),
					  )
	fitbiter.save()
	
	##Get Initial FitbitData
	FitbitURL='https://api.fitbit.com/1/user/'+fitbiter.fitbit_id+'/activities/distance/date/today/7d.json'
 	
	req=urllib.request.Request(FitbitURL)
	req.add_header('Authorization', 'Bearer ' + fitbiter.access_token)
	
	response=urllib.request.urlopen(req)
	FullResponse=response.read()
	ResponseJSON = json.loads(FullResponse)
	
	activity_data=ResponseJSON
	distance_by_date=activity_data['activities-distance']
	for i in distance_by_date:
		fitdata=FitData(fitbiter=fitbiter,
				date=i['dateTime'],
				distance=i['value'],
				)
		fitdata.save()
	
	##Get Initial FitbitDeviceInfo
	FitbitDeviceURL='https://api.fitbit.com/1/user/'+fitbiter.fitbit_id+'/devices.json'
	
	devicereq=urllib.request.Request(FitbitDeviceURL)
	devicereq.add_header('Authorization', 'Bearer ' + fitbiter.access_token)
	
	deviceresponse=urllib.request.urlopen(devicereq)
	deviceFullResponse=deviceresponse.read()
	deviceResponseJSON = json.loads(deviceFullResponse)
	
	device_data=deviceResponseJSON
	
	#Not sure what will happen if more than one device
	for d in device_data:
		last_sync=d['lastSyncTime']
		formatted_last_sync=datetime.strptime(last_sync, '%Y-%m-%dT%H:%M:%S.%f')
		fitbiter.last_sync=formatted_last_sync
		fitbiter.save()
		
	##Stupid hack as needs to be iterable for FitData to Display
	fitbiter_ids=[]
	fitbiter_ids.append(fitbiter.pk)
	
	#Displays the fitbiters data
	return redirect(reverse('fitdata-display', kwargs={'fitbiter_ids':fitbiter_ids,'num_days':5}))