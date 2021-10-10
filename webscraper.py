import requests
from bs4 import BeautifulSoup

steamUrl = 'https://store.steampowered.com/search/?term='
winGameUrl = 'https://www.wingamestore.com/search/?SearchWord='
GOGUrl = 'https://www.gog.com/games?search='
humbleUrl = 'https://www.humblebundle.com/store/search?sort=bestselling&search='

class GameDetails:
    def __init__(game):
        game.gameTitle = "No game found."
        game.originalPrice = 0
        game.discountedPrice = 0
        game.discountPct = 0
        game.store = "Store"

def scrapeSteam(searchTerm):
    page = requests.get(steamUrl + searchTerm)
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

def displayInfo(arr):
    STORE = "{txt:^18}".format(txt = "Store")
    GAME_TITLE = "{txt:^50}".format(txt = "Game Title")
    ORIGINAL_PRICE = "{txt:^20}".format(txt = "Original Price")
    DISCOUNTED_PRICE = "{txt:^20}".format(txt = "Discounted Price")
    DISCOUNT_PERCENT = "{txt:^20}".format(txt = "Discount Percent")
    print(STORE, GAME_TITLE, ORIGINAL_PRICE, DISCOUNTED_PRICE, DISCOUNT_PERCENT, sep = "|")
    print("------------------------------------------------------------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------------------------------------------------------------")

    # iterate through all scrapes
    for game in arr:
        print(
            "{txt:^18}".format(txt = game.store), 
            "{txt:^50}".format(txt = game.gameTitle), 
            "{txt:^20}".format(txt = game.originalPrice), 
            "{txt:^20}".format(txt = game.discountedPrice), 
            "{txt:^20}".format(txt = game.discountPct), 
            sep = "|"
        )
        print("------------------------------------------------------------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------------------------------------------------------------")

print("Enter the name of a game:")
stringInput = input()
searchTerm = stringInput.lower()

steamGame = scrapeSteam(searchTerm)

games = []
games.append(steamGame)
games.append(steamGame)

displayInfo(games)

