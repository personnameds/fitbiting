from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from fitbiters.models import Fitbiter
from fitdata.models import FitData
from django.conf import settings
from django.db import IntegrityError

import requests #need to install this library

import base64
import urllib
import json

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


CLIENT_DIRECTORY=os.path.join(BASE_DIR,'fitbiting')+'/CLIENT_ID'
with open(CLIENT_DIRECTORY) as f:
    CLIENT_ID = f.read().strip()

CLIENT_DIRECTORY=os.path.join(BASE_DIR,'fitbiting')+'/CLIENT_SECRET'
with open(CLIENT_DIRECTORY) as f:
    CLIENT_SECRET = f.read().strip()


client_id=CLIENT_ID
client_secret=CLIENT_SECRET

token_url='https://api.fitbit.com/oauth2/token'


def GetFitbitData(fitbiter):
	
	data=GetDataUsingAccessToken(fitbiter) 
	return data
    

def GetDataUsingAccessToken(fitbiter):

	try: 
		last_date=FitData.objects.filter(fitbiter=fitbiter).latest('date').date
		FitData.objects.filter(fitbiter=fitbiter, date=last_date).delete()
		last_date=last_date.strftime("%Y-%m-%d")
		FitbitURL='https://api.fitbit.com/1/user/'+fitbiter.fitbit_id+'/activities/distance/date/'+last_date+'/today.json'
	except IndexError:
		FitbitURL='https://api.fitbit.com/1/user/'+fitbiter.fitbit_id+'/activities/distance/date/today/1d.json'
 	
	req=urllib.request.Request(FitbitURL)
	req.add_header('Authorization', 'Bearer ' + fitbiter.access_token)
	
	try:
		response=urllib.request.urlopen(req)
		FullResponse=response.read()
		
		ResponseJSON = json.loads(FullResponse)

		return(ResponseJSON)
	
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


def Oauth2View(request):
	authorize_url='https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=22CVHF&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Foauth2callback&scope=activity&expires_in=604800'
	return HttpResponseRedirect(authorize_url)


def Oauth2CallBackView(request):
	code=request.GET.get('code')
	
	##To Get Access and Refresh Token
	BodyText={'code':code,
			  'redirect_uri':'http://localhost:8000/oauth2/oauth2callback',
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

	fitbit_id=str(ResponseJSON['user_id'])

	if Fitbiter.objects.filter(fitbit_id=fitbit_id).exists():
		return redirect('fitdata-index')
		##return redirect('getfitdata-view', fitbiter=Fitbiter.objects.get(fitbit_id=fitbit_id))
	else:
		fitbiter=Fitbiter(fitbit_id=fitbit_id,
				          access_token=str(ResponseJSON['access_token']),
					  	  refresh_token=str(ResponseJSON['refresh_token']),
					      )
		fitbiter.save()
	
	##Used to get data immediately
	##return redirect('getfitdata-view', fitbiter=fitbiter.fitbit_id)
	##now goes to fitdata index and downloads data... I think
	return redirect('fitdata-index') 