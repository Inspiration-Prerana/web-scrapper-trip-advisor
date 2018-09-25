import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter

name = []
price = []
provider = []
review = []
rating = []
link = []
wifi = []
breakfast = []
parking = []
restaurant = []
t = "true"
f = "false"
n = 0
location = ["g293890-Kathmandu_Kathmandu_Valley_Bagmati_Zone_Central_",
            "g293891-Pokhara_Gandaki_Zone_Western_",
            "g315764-Patan_Lalitpur_Kathmandu_Valley_Bagmati_Zone_Central_",
            "g424934-Bhaktapur_Kathmandu_Valley_Bagmati_Zone_Central_",
            "g424940-Lumbini_Lumbini_Zone_Western_",
            "g293892-Chitwan_National_Park_Chitwan_District_Narayani_Zone_Central_",
            "g317113-Dhulikhel_Bagmati_Zone_Central_",
            "g1207740-Hetauda_Makwanpur_Narayani_Zone_Central_"
            ]


def scrape(weblink, x):
    print(weblink)
    x = x + 1
    print(x)
    page = requests.get(weblink)
    soup = BeautifulSoup(page.content, 'html.parser')

    hotel_containers = soup.find_all('div', class_='listItem')
    print(type(hotel_containers))
    print(len(hotel_containers))

    for container in hotel_containers:
        ex_name = container.find(class_="listing_title")
        print(ex_name.a.text)
        name.append(ex_name.a.text)
        ex_link = ex_name.a
        lnk = "https://www.tripadvisor.com" + ex_link.get("href")
        link.append(lnk)

        try:
            ex_price = container.find(class_="price-wrap")
            print(ex_price.div.text)
            price.append(ex_price.div.text)
        except AttributeError:
            price.append(0)

        try:
            ex_provider = container.find(class_="provider")
            print(ex_provider.text)
            provider.append(ex_provider.text)
        except AttributeError:
            provider.append("no provider")

        try:
            ex_review = container.find(class_="review_count")
            print(ex_review.text)
            review.append(ex_review.text)
        except AttributeError:
            review.append(0)

        try:
            ex_rating = container.find(class_="ui_bubble_rating")
            print(ex_rating.get('alt', 'No rating'))
            rating.append(ex_rating.get('alt', 'No rating'))
        except AttributeError:
            rating.append(0)

        try:
            ex_wifi = container.find(class_="wifi").text
            print(t)
            wifi.append(t)
        except AttributeError:
            print(f)
            wifi.append(f)

        try:
            ex_breakfast = container.find(class_="coffee-tea-cafe").text
            breakfast.append(t)
        except AttributeError:
            breakfast.append(f)

        try:
            ex_parking = container.find(class_="parking").text
            parking.append(t)
        except AttributeError:
            parking.append(f)

        try:
            ex_restro = container.find(class_="restaurants").text
            restaurant.append(t)
        except AttributeError:
            restaurant.append(f)

    try:
        next_ = soup.find("a", class_="next")
        print("https://www.tripadvisor.com" + next_.get("href"))
        if x > 20:
            return
        else:
            scrape("https://www.tripadvisor.com" + next_.get("href"), x)
    except AttributeError:
        return


for loc in location:
    url = "https://www.tripadvisor.com/Hotels-" + loc + "Region-Hotels.html"
    print(url)
    scrape(url, n)

hotel_df = pd.DataFrame({'Name': name,
                         'Price': price,
                         'Provider': provider,
                         'Review': review,
                         'Rating': rating,
                         'Link': link,
                         'Wifi': wifi,
                         'Breakfast': breakfast,
                         'Parking': parking,
                         'Restaurant': restaurant})
print(hotel_df.info())
print(hotel_df)
hotel_df.to_csv('scrap_hotel.csv', sep='\t', encoding='utf-8')
writer = ExcelWriter('scrap_hotel.xlsx')
hotel_df.to_excel(writer, 'Sheet5')
writer.save()
