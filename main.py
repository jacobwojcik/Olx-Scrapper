import requests
from bs4 import BeautifulSoup
from csv import writer
import pprint

#UI

print("Welcome to Olx Web-Scrapper!")
searchFor=input('What are you looking for? ').lower()
city=input('City: ').lower()
minPrice=input('Minimal price: ')
maxPrice=input('Max price: ')

#request
pageUrl="https://www.olx.pl/"+city+"/q-"+searchFor+"/?search[filter_float_price%3Afrom]="+minPrice+"&search[filter_float_price%3Ato]="+maxPrice
page = requests.get(pageUrl)
soup = BeautifulSoup(page.content, 'html.parser')
links=soup.find_all("a", class_="marginright5 link linkWithHash detailsLink")
# deleting tags

def deleteTags(x):
    x = str(x).replace('<strong>', '')
    x = str(x).replace('</strong>', '')
    return x


localName = list(soup.select("h3 strong"))
localName = list(map(deleteTags, localName))
localPrice = list(soup.select("p strong"))
localPrice = list(map(deleteTags, localPrice))

listOfLocals = dict()

for i in localName:
    listOfLocals[i] = localPrice[localName.index(i)]

pprint.sorted = lambda x, key=None: x

pprint.pprint(listOfLocals)


print("-----------------")
writeToCsv=input("Would you like to save offers into csv file? y/n : ")

if writeToCsv=="y":
    with open('offers.csv', 'w') as csv_file:
        csv_writer=writer(csv_file)
        headers = ["Offer", "Price"]
        csv_writer.writerow(headers)

        for offer in listOfLocals:
            csv_writer.writerow([offer,listOfLocals[offer]])


