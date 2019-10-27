from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .models import Platform
from runners.models import Fitbiter, Runner, Stravaer
from rundata.models import RunData
from django.conf import settings
from django.db import IntegrityError
from django.urls import reverse

import requests #need to install this library
from datetime import datetime
import base64
import urllib
import json

import os

def UpdateRunData(runner, update_date):
	GetDataUsingAccessToken(runner, update_date) 
	return
    
def GetDataUsingAccessToken(runner, update_date):

	#Erase the data from that date
	#Then get new data from the date and beyond
	RunData.objects.filter(runner=runner, date__gte=update_date).delete()
	last_date=update_date.strftime("%Y-%m-%d")
	
	##Fitbit
	if runner.platform.name == 'Fitbit':
		fitbiter=Fitbiter.objects.get(runner=runner)
	
		FitbitURL='https://api.fitbit.com/1/user/'+fitbiter.fitbit_id+'/activities/distance/date/'+last_date+'/today.json'
		req=urllib.request.Request(FitbitURL)
		req.add_header('Authorization', 'Bearer ' + fitbiter.access_token)
	
		try:
			response=urllib.request.urlopen(req)
			FullResponse=response.read()
			activity_data = json.loads(FullResponse)
			distance_by_date=activity_data['activities-distance']
			for i in distance_by_date:
				rundata=RunData(runner=runner,
					date=i['dateTime'],
					distance=i['value'],
					)
				rundata.save()	
			return
		except urllib.request.URLError as e:
			HTTPErrorMessage=str(e.read())
			##If Access token Expired
			if (e.code==401) and (HTTPErrorMessage.find("Access token expired") > 0):
				GetNewAccessandRefreshToken(runner, update_date)
			## Some other error
			else:
				print(e.code)
				print(e.read())
				return False

	##Strava
	elif runner.platform.name == 'Strava':

		stravaer=Stravaer.objects.get(runner=runner)

		StravaURL='https://www.strava.com/api/v3/athlete/activities'
		req=urllib.request.Request(StravaURL)
		req.add_header('Authorization', 'Bearer ' + stravaer.access_token)
		
		try:
			response=urllib.request.urlopen(req)
			FullResponse=response.read()
			ResponseJSON=json.loads(FullResponse)
			for activity_data in ResponseJSON:
				distance=activity_data['distance']/1000
				date=datetime.strptime(activity_data['start_date_local'],"%Y-%m-%dT%H:%M:%SZ")
				if date.date() >= update_date:
					rundata=RunData(runner=runner,
						date=date.date(),
						distance=distance,
						)
					rundata.save()
		except urllib.request.URLError as e:
			HTTPErrorMessage=str(e.read())
			##If Access token Expired
			if (e.code==401) and (HTTPErrorMessage.find("Authorization Error") > 0):
				GetNewAccessandRefreshToken(runner, update_date)
			## Some other error
			else:
				print(HTTPErrorMessage)
				return False

def GetNewAccessandRefreshToken(runner, update_date):
	platform=Platform.objects.get(id=runner.platform.id)
	client_id=platform.client_id
	client_secret=platform.client_secret

	if platform.name == 'Fitbit':
		token_url='https://api.fitbit.com/oauth2/token'

		fitbiter=runner.fitbiter
		
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

	elif platform.name=='Strava':
		token_url='https://www.strava.com/api/v3/oauth/token'
		
		stravaer=runner.stravaer

		##Use Refresh token to get new  access token
		BodyText={'client_id': client_id,
			  'client_secret': client_secret,
			  'grant_type':'refresh_token',
			  'refresh_token':stravaer.refresh_token,
			  }
		BodyURLEncoded=urllib.parse.urlencode(BodyText).encode()
		req=urllib.request.Request(token_url,BodyURLEncoded)	
		try:
			response=urllib.request.urlopen(req)
			FullResponse=response.read()
			print('Strava Refresh Token Success')
		except urllib.request.URLError as e:
			print('Strava Refresh Token Error')
			print(e.code)
			print(e.read())
			
		## Access and Refresh Token Received
		## Saving tokens to model
		ResponseJSON = json.loads(FullResponse)

		stravaer.access_token = str(ResponseJSON['access_token'])
		stravaer.refresh_token = str(ResponseJSON['refresh_token'])
		stravaer.save()
		
	GetDataUsingAccessToken(runner, update_date)

##New User
def NewRunnerView(request, platform_id):

	platform=Platform.objects.get(id=platform_id)
	client_id=platform.client_id
	redirect_uri=platform.redirect_uri
		
	redirect_uri=urllib.parse.quote(redirect_uri, safe='')
	
	if platform.name == 'Fitbit':	
		authorize_url='https://www.fitbit.com/oauth2/authorize?response_type=code&client_id='+client_id+'&redirect_uri='+redirect_uri+'&scope=activity&expires_in=86400'
	elif platform.name == 'Strava':
		authorize_url='https://www.strava.com/oauth/authorize?client_id='+client_id+'&response_type=code&redirect_uri='+redirect_uri+'&approval_prompt=auto&scope=activity:read_all'
	return HttpResponseRedirect(authorize_url)

def StravaCallBackView(request):

	platform=Platform.objects.get(name='Strava')
	client_id=platform.client_id
	client_secret=platform.client_secret
	redirect_uri=platform.redirect_uri

	token_url='https://www.strava.com/api/v3/oauth/token'
	
	code=request.GET.get('code')
	
	##To Get Access and Refresh Token
	BodyText={'code':code,
			  'client_id': client_id,
			  'client_secret': client_secret,
			  'grant_type':'authorization_code',
			  }
	BodyURLEncoded=urllib.parse.urlencode(BodyText).encode()
	
	req=urllib.request.Request(token_url,BodyURLEncoded)
	
	try:
		response=urllib.request.urlopen(req)
		FullResponse=response.read()

	except urllib.request.URLError as e:
		print(e.code)
		print(e.read())
		
	## Access and Refresh Token Received
	## Saving tokens to model
	ResponseJSON = json.loads(FullResponse)

	runner=Runner.objects.get(user=request.user)

	athlete=ResponseJSON['athlete']
	strava_id=athlete['id']

	stravaer=Stravaer(runner=runner,
				      strava_id=str(strava_id),
					  access_token=str(ResponseJSON['access_token']),
					  refresh_token=str(ResponseJSON['refresh_token']),
					  )
	stravaer.save()

	##Get Initial FitbitData
	StravaURL='https://www.strava.com/api/v3/athlete/activities'
	req=urllib.request.Request(StravaURL)
	req.add_header('Authorization', 'Bearer ' + stravaer.access_token)
	
	try:
		response=urllib.request.urlopen(req)
		FullResponse=response.read()
	except urllib.request.URLError as e:
		print(e.code)
		print(e.read())
		
	ResponseJSON = json.loads(FullResponse)

	for activity_data in ResponseJSON:
		distance=activity_data['distance']/1000
		date=datetime.strptime(activity_data['start_date_local'],"%Y-%m-%dT%H:%M:%SZ")
		rundata=RunData(runner=runner,
			date=date.date(),
			distance=distance,
			)
		rundata.save()
 
	#Displays the runners data	
	return redirect(reverse('rundata-display', kwargs={'runner_ids':[runner.pk,],'num_days':5}))


def FitbitCallBackView(request):

	platform=Platform.objects.get(name='Fitbit')
	client_id=platform.client_id
	client_secret=platform.client_secret
	redirect_uri=platform.redirect_uri

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

	except urllib.request.URLError as e:
		print(e.code)
		print(e.read())
		
	## Access and Refresh Token Received
	## Saving tokens to model
	ResponseJSON = json.loads(FullResponse)

	runner=Runner.objects.get(user=request.user)

	fitbiter=Fitbiter(runner=runner,
				      fitbit_id=str(ResponseJSON['user_id']),
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
		rundata=RunData(runner=runner,
				date=i['dateTime'],
				distance=i['value'],
				)
		rundata.save()

	#Displays the runners data	
	return redirect(reverse('rundata-display', kwargs={'runner_ids':[runner.pk,],'num_days':5}))