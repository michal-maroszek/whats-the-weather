import requests
import json
from geopy.geocoders import Nominatim
import datetime as dt

today = dt.date.today()

# Getting coordinates based on user input (City name)
location = Nominatim(user_agent='GetLoc')
getLocation = location.geocode(input('Enter the name of a city: '))

lat = getLocation.latitude
lon = getLocation.longitude

# Using air quality API to get current air pollution parameters based on user location and current date
url_pollution = f'https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=pm10,pm2_5,carbon_monoxide&timezone=Europe%2FLondon&start_date={today}&end_date={today}'
url_weather = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,apparent_temperature,precipitation,surface_pressure,windspeed_10m&daily=uv_index_max&forecast_days=1&start_date={today}&end_date={today}&timezone=Europe%2FLondon'

response_pollution = requests.get(url_pollution)
data_pollution = json.loads(response_pollution.text)

response_weather = requests.get(url_weather)
data_weather = json.loads(response_weather.text)

# Extracting specific data from given json file
data_pm2_5 = data_pollution['hourly']['pm2_5']
data_pm10 = data_pollution['hourly']['pm10']
data_carbon_monoxide = data_pollution['hourly']['carbon_monoxide']

data_temperature = data_weather['hourly']['temperature_2m']
data_apparent_temperature = data_weather['hourly']['apparent_temperature']
data_pressure = data_weather['hourly']['surface_pressure']
data_wind = data_weather['hourly']['windspeed_10m']
data_rain = data_weather['hourly']['precipitation']
data_uv_index_max = data_weather['daily']['uv_index_max']

data_day_time = data_weather['hourly']['time']


def day_time(day_time_list):

    for value in day_time_list:
        day_time_separated = value.split('T')
        return day_time_separated[0], day_time_separated[1]


def hourly_pollution(pm2_5, pm10, co):

    # Takes extracted data about hourly pollution levels, prints them out, and qualify them.

    hour = -1
    # Hour is set to -1 so the counting starts from hour 0:00
    for value in pm2_5:
        hour += 1
        if value <= 10:
            air_condition = 'Good'
        elif 20 > value > 10:
            air_condition = 'Fair'
        elif 25 > value > 20:
            air_condition = 'Moderate'
        elif 50 > value > 25:
            air_condition = 'Poor'
        elif 75 > value > 50:
            air_condition = 'Very poor'
        elif value > 75:
            air_condition = 'Extremely poor'

        print(f'Hour:{hour} - PM2.5 = {value}    Quality index: {air_condition}')

    hour = -1
    for value in pm10:
        hour += 1
        if value <= 20:
            air_condition = 'Good'
        elif 40 > value > 20:
            air_condition = 'Fair'
        elif 50 > value > 40:
            air_condition = 'Moderate'
        elif 100 > value > 50:
            air_condition = 'Poor'
        elif 150 > value > 100:
            air_condition = 'Very poor'
        elif value > 150:
            air_condition = 'Extremely poor'

        print(f'Hour:{hour} - PM10 = {value}    Quality index: {air_condition}')

    hour = -1
    for value in co:
        hour += 1
        print(f'Hour:{hour} - CO = {value}')


def daily_pollution(pm2_5, pm10, co):

    sum_pm25 = 0
    num_of_values = 0
    for value in pm2_5:
        sum_pm25 += value
        num_of_values += 1

    daily_pm25 = round(sum_pm25 / num_of_values, 2)
    print(f'Average daily PM 2.5 pollution level: {daily_pm25}')

    sum_pm10 = 0
    num_of_values = 0
    for value in pm10:
        sum_pm10 += value
        num_of_values += 1

    daily_pm10 = round(sum_pm10 / num_of_values, 2)
    print(f'Average daily PM 10 pollution level: {daily_pm10}')

    sum_co = 0
    num_of_values = 0
    for value in co:
        sum_co += value
        num_of_values += 1

    daily_co = round(sum_co / num_of_values, 2)
    print(f'Average daily CO pollution level: {daily_co}')


def daily_weather(temperature, apparent_temperature, pressure, rain, windspeed, uv_index):
    pass

# daily_pollution(data_pm2_5, data_pm10, data_carbon_monoxide)
day_time(data_day_time)
