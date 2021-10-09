import requests
from bs4 import BeautifulSoup

steamUrl = 'https://store.steampowered.com/search/?term='
winGameUrl = 'https://www.wingamestore.com/search/?SearchWord='
GOGUrl = 'https://www.gog.com/games?search='
humbleUrl = 'https://www.humblebundle.com/store/search?sort=bestselling&search='

stringInput = 'chILDREN OF morta' #user input here
searchTerm = stringInput.lower()

page = requests.get(steamUrl + searchTerm)
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id = "search_resultsRows")

if (results != None):
    res = results.find_all("a")
    gameTitle = res[0].find("span", class_ = "title").string.lower()

    if (gameTitle == searchTerm):
        originalPrice = res[0].find("strike").string

        discountDiv = res[0].find("div", class_ = "col search_price discounted responsive_secondrow")
        discountDiv.span.extract()
        discountDiv.br.extract()
        discountedPrice = discountDiv.text

        pctDiv = res[0].find("div", class_ = "col search_price_discount_combined responsive_secondrow")
        discountPct = pctDiv.find("span").string

        # output here
        print("original price -->", originalPrice)
        print("discounted price -->", discountedPrice)
        print("discount -->", discountPct)
    else:
        print('WRONG GAME') # output
