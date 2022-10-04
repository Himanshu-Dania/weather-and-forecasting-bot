import requests
import discord
import os
import requests
from datetime import date

key=os.environ['key']
client = discord.Client(intents=discord.Intents.all())
#for aqi
us_index={
  1:"Good",
2:"Moderate",
3:"Unhealthy for sensitive group",
4:"Unhealthy",
5:"Very Unhealthy",
6:"Hazardous"
}
#for aqi
uk_index={
  1:"Low Pollution",
2:"Low Pollution",
3:"Low Pollution",
4:"Medium Pollution",
5:"Medium Pollution",
6:"Medium Pollution",
7:"High Pollution",
  8:"High Pollution",
  9:"High Pollution",
  10:"Very High Pollution"
}
def alerts(name):
  url_alerts="http://api.weatherapi.com/v1/forecast.json"
  params={
    'key':key,
    'q':name,
    'alerts':'yes'
  }
  response=requests.get(url_alerts,params=params).json()
  l=len(response['alerts']['alert'])
  s=''
  for i in range(l):
    s+='**```'
    s+=("Headline:-" + response['alerts']['alert'][i]['headline']+"\n")
    s+=("Severity :-" + response['alerts']['alert'][i]['severity']+'\n') 
    s+=("Certainty :-" + response['alerts']['alert'][i]['certainty']+'\n') 
    s+=("Note :-" + response['alerts']['alert'][i]['note']+'\n') 
    s+=("Effective from :-"+response['alerts']['alert'][i]['effective']+'\n') 
    s+=("Expires at :-" + response['alerts']['alert'][i]['expires'])
    s+='```**'
    s+='\n\n'
  return s
def fore(name,i):
  url_forecast="http://api.weatherapi.com/v1/forecast.json"
  params={
      'key':key,
      'q':name,
      'days':i+1
  }
  response=requests.get(url_forecast,params=params).json()
  return ('**```'+response['location']['name']+'\n'+'Date:-'+str(response['forecast']['forecastday'][i]['date'])+"\n"+"Average Temperature(C) :-"+str(response['forecast']['forecastday'][i]['day']['avgtemp_c'])+'\n'+"Maximum Windspeed(kph):-"+(str(response['forecast']['forecastday'][i]['day']['maxwind_kph']))+"\n"+'Total Precipiation(mm):-'+str(response['forecast']['forecastday'][i]['day']['totalprecip_mm'])+'\n'+'Average Visibility(km):- '+str(response['forecast']['forecastday'][i]['day']['avgvis_km'])+'\n'+'Average Humidity in %:-'+str(response['forecast']['forecastday'][i]['day']['avghumidity'])+'\n'+'will it rain:-'+str(response['forecast']['forecastday'][i]['day']['daily_will_it_rain'])+'\n'+'Chance of rain in %:-'+str(response['forecast']['forecastday'][i]['day']['daily_chance_of_rain'])+'\n'+'will it snow:-'+str(response['forecast']['forecastday'][i]['day']['daily_will_it_snow'])+'\n'+'Chance of snow in %:-'+str(response['forecast']['forecastday'][i]['day']['daily_chance_of_snow'])+'\n'+str(response['forecast']['forecastday'][i]['day']['condition']['text'])+'```**'+'\n'+'http:'+str(response['forecast']['forecastday'][i]['day']['condition']['icon']))
'][i]['day']['condition']['icon']))

def fetchaqi(name, i):
  url_forecast="http://api.weatherapi.com/v1/forecast.json "
  params={
      'key':key,
      'q':name,
      'days':i+1,
      'aqi':'yes'
  }
  response=requests.get(url_forecast,params=params).json()
  return "**```"+str('Name:-'+response['location']['name']+'\n'+'Region:-'+response['location']['region']+'\n'+ "Carbon Monoxide in the air(μg/m3) :-" + response['forecast']['forecastday'][i]['day']['air_quality']['co'])+"\n"+"Nitrogen dioxide in the air (μg/m3) :-" +  str(response['forecast']['forecastday'][i]['day']['air_quality']['no2'])+"\n"+"Ozone in the air(μg/m3) :- " +  str(response['forecast']['forecastday'][i]['day']['air_quality']['o3'])+"\n"+ "Sulphur Dioxide in the air (μg/m3) :- " + str(response['forecast']['forecastday'][i]['day']['air_quality']['so2'])+"\n"+"PM 2.5 in the air (μg/m3) :- " + str(response['forecast']['forecastday'][i]['day']['air_quality']['pm2_5'])+"\n"+"PM 10 in the air (μg/m3) :- " + str(response['forecast']['forecastday'][i]['day']['air_quality']['pm10'])+"\n"+ "The US EPA Index is :- " + str(response['forecast']['forecastday'][i]['day']['air_quality']['us-epa-index'])+" - "+us_index[response['forecast']['forecastday'][i]['day']['air_quality']['us-epa-index']]+"\n"+"THE UK Debra Index is :- "+ str(response['forecast']['forecastday'][i]['day']['air_quality']['gb-defra-index'])+' - '+uk_index[response['forecast']['forecastday'][i]['day']['air_quality']['gb-defra-index']]+"```**"
def fetchdata(name):
  url="http://api.weatherapi.com/v1/current.json"
  today=date.today()
  params={
      'key':key, 
      'q':name,
  }
  response = requests.get(url,params=params).json()
  return ("**```"+'Name:-'+response['location']['name']+'\n' 
+'Region:-'+response['location']['region']+'\n'+'Country:-'+response['location']['country'] +'\n'+'Localtime:-'+str(response['location']['localtime'])+'\n'+"The temperature (C) is:-"+str(response['current']['temp_c'])+'\n'+"Current wind speed(kph):-"+str(response['current']['wind_kph'])+'\n'+"Current pressure(mb):-"+str(response['current']['pressure_mb'])+'\n'+"The humidity % is:-"+str(response['current']['humidity'])+'\n'+"Cloud cover as % is:- "+str(response['current']['cloud'])+'\n'+"visibility:-"+response['current']['condition']['text']+"\n"+"The UV Index is :-" + str(response['current']['uv'])+'\n'+"precipiation in mm:-"+str(response['current']['precip_mm'])+'```**'+'\n'+"http:"+response['current']['condition']['icon'])


@client.event
async def on_ready():
   print('We have logged in as {0.user}'.format(client))
@client.event
async def on_message(message):
  if message.author== client.user:
    return 
  msg=message.content
 #WEATHER FUNC
  if msg.startswith("?weather"):
      word=msg.split()
      important_word=word[1:]
      try:
        await message.channel.send(fetchdata(important_word))
      except KeyError as ve:
        await message.channel.send("**``Enter a valid location``**")
#FORECAST FUNC
  elif msg.startswith("?forecast"):
      words=msg.split()
      
      try:
        c=int(words[len(words)-1])
        if isinstance(c, int):
         important_wordd=words[1:]
         await message.channel.send(fore(important_wordd,c))
        else:
         await message.channel.send("**```Enter a number after location-name. Check ?help for more```**")
      except (ValueError,IndexError,KeyError)as ve:
         await message.channel.send("**``` Enter a number after location-name. Check ?help for more ```**")
#HELP FUNC
  elif msg.startswith('?help'):
    await message.channel.send('**```Commands:\n1.?weather:- Writing "?weather location-name" will give you the current weather of location entered.\n2.?forecast:- Writing "?forecast location-name index" gives you the weather forecast of the day.\nIndex=0 refers to the current day. Index=1 refers to tomorrow and so on. Index has to lie between 0-13.\n3.?aqi:- Writing "?aqi location-name index" gives you the air quality index of the day.\nIndex=0 refers to the current day. Index=1 refers to tomorrow and so on. Index has to lie between 0-13.\n4.?alerts:- Writing "?alerts location-name" tells you if there are any safety alerts going on in that location."```**')
#AIR QUALITY FUNC
  elif msg.startswith('?aqi'):
    words=msg.split()
    try:
        p=int(words[len(words)-1])
        if isinstance(p, int):
         important_worddd=words[1:]
         await message.channel.send(fetchaqi(important_worddd,p))
        else:
         await message.channel.send("**```Enter a number after location-name. Check ?help for more```**")
    except (ValueError,IndexError,KeyError)as ve:
         await message.channel.send("**``` Enter a number after location-name. Check ?help for more ```**")
  elif msg.startswith('?alerts'):
    word=msg.split()
    important_wordddd=word[1:]
    
    try:
      if len(important_wordddd)==0 or isinstance(important_wordddd[0], int):
        await message.channel.send("**``Enter a valid location``**")
      else: 
        await message.channel.send(alerts(important_wordddd))
    except (discord.errors.HTTPException)as a:
        await message.channel.send("**``This location does not have any alerts going on right now. ``**")
    except KeyError as b:
      await message.channel.send("**``Enter a valid location``**")

    
client.run(os.environ['TOKEN'])
    
