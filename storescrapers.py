import requests
from bs4 import BeautifulSoup

STEAM_URL = 'https://store.steampowered.com/search/?term='
WINGAME_URL = 'https://www.wingamestore.com/search/?SearchWord='
GOG_URL = 'https://www.gog.com/games?search='
HUMBLE_URL = 'https://www.humblebundle.com/store/search?sort=bestselling&search='

class GameDetails:
    '''Game data object'''
    def __init__(self):
        self.gameTitle = "No game found."
        self.originalPrice = 0
        self.discountedPrice = 0
        self.discountPct = 0
        self.store = "Store"

def scrapeSteam(searchTerm):
    page = requests.get(STEAM_URL + searchTerm)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id = "search_resultsRows")

    steamGame = GameDetails()
    steamGame.store = "Steam"

    if (results != None):
        res = results.find_all("a")
        steamGame.gameTitle = res[0].find("span", class_ = "title").string

        priceDiv = res[0].find("div", class_ = "col search_price_discount_combined responsive_secondrow")
        pctDiv = priceDiv.find("div", class_ = "col search_discount responsive_secondrow")
        hasStrike = res[0].find("strike")
        if (hasStrike):
            steamGame.discountPct = pctDiv.find("span").string
            steamGame.originalPrice = hasStrike.string.strip()

            discountDiv = res[0].find("div", class_ = "col search_price discounted responsive_secondrow")
            discountDiv.span.extract()
            discountDiv.br.extract()
            steamGame.discountedPrice = discountDiv.text.strip()
        else:
            steamGame.originalPrice = res[0].find("div", class_ = "col search_price responsive_secondrow").string.strip()
    
    return steamGame