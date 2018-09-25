from bs4 import BeautifulSoup
import requests
import pandas as pd
import geocoder
from pandas import ExcelWriter
df = pd.read_csv('scrap_hotel.csv', sep='\t', encoding='utf-8')
saved_column = df.Link

strt = []
ext = []
local = []
n = 0
latitude = []
longitude = []
for url in saved_column:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(n)
    n = n + 1

    detail = soup.find('span', class_='detail')
    print(detail.text)
    g = geocoder.google(detail.text)
    print(g.lat)
    print(g.lng)
    latitude.append(g.lat)
    longitude.append(g.lng)
    try:
        street = detail.find('span', class_='street-address')
        strt.append(street.text)
        #print(street.text)
    except AttributeError:
        strt.append(" ")
    try:
        extended = detail.find('span', class_='extended-address')
        ext.append(extended.text)
        #print(extended.text)
    except AttributeError:
        ext.append(" ")
    try:
        locality = detail.find('span', class_='locality')
        local.append(locality.text)
        #print(locality.text)
    except AttributeError:
        local.append(" ")

location_df = pd.DataFrame({'StreetAddress': strt,
                            'ExtendedAddress': ext,
                            'Locality': local,
                            'Latitude': latitude,
                            'Longitude': longitude
                            })
print(location_df.info())
print(location_df)
location_df.to_csv('location_hotel.csv', sep='\t', encoding='utf-8')
writer = ExcelWriter('location_hotel.xlsx')
location_df.to_excel(writer, 'Sheet5')
writer.save()
