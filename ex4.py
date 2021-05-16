# -*- coding: utf-8 -*-
"""
Created on Sun May 16 10:40:15 2021

@author: o
"""

import requests

apikey = " " #Uploaded to the Moodle


def get_distance(data, origin_data, apikey):
    origin_lat = origin_data['lat']
    origin_lng = origin_data['lng']
    dest_lat = data['lat']
    dest_lng = data['lng']
    origin = "origins="+origin_lat+","+origin_lng
    destination = "destinations="+dest_lat+","+dest_lng
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"+origin+"&"+destination+"&key="+apikey
    response = requests.get(url).json()
    rows = response['rows'][0]
    element = rows['elements'][0]
    distance_meter = element['distance']['value']
    distance_km = distance_meter/1000
    data['distance'] = str(distance_km)+' km'
    duration = element['duration']['text']
    data['duration'] = duration


def get_location(city, data, apikey):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + city + "&key=" + apikey
    response = requests.get(url).json()
    result = response["results"]
    geometry_data = result[0]['geometry']
    location = geometry_data['location']
    lat = location['lat']
    lng = location['lng']
    data['lat'] = lat
    data['lng'] = lng
    return data


fhand = open('dests.txt', 'r', encoding='UTF-8')
origin = 'תל אביב'
city_data = dict()
data_to_append = list()
all_data = dict()
origin_data = dict()
get_location(origin, origin_data)
for line in fhand.readlines():
    city = line.strip()
    try:
        get_location(city, city_data)
        get_distance(city_data, origin_data)
        for d in city_data:
            data_to_append.append(d+": "+city_data[d])
        all_data[city] = tuple(data_to_append)
        print(str(all_data))
        break
    except Exception as e:
        print(str(e))
        break
    finally:
        fhand.close()
