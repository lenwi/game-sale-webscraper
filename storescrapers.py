import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

STEAM_URL = 'https://store.steampowered.com/search/?term='
FANATICAL_URL = 'https://www.fanatical.com/en/search?search='
GOG_URL = 'https://www.gog.com/games?search='
HUMBLE_URL = 'https://www.humblebundle.com/store/search?sort=bestselling&search='

class GameDetails:
    '''
    Game data object\n
    gameTitle       -> "Children of Morta"\n
    originalPrice   -> "CDN$ 28.99"\n
    discountedPrice -> "CDN$ 11.59"\n
    discountPct     -> "-60%"
    '''
    def __init__(self):
        self.gameTitle = "No game found."
        self.originalPrice = 0
        self.discountedPrice = 0
        self.discountPct = 0
        self.store = "Store"

def handleError(store):
    failedGame =  GameDetails()
    failedGame.store = store
    failedGame.gameTitle = "DOWN"
    return failedGame

def scrapeSteam(searchTerm):
    try:
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
    except Exception as error:
        print(error)
        return handleError("Steam")

def scrapegog(searchTerm):
    try:
        # chromium headless webdriver to get js content
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--incognito")
        options.add_argument("--log-level=3") # hides garbage from console
        driver = webdriver.Chrome(options = options)
        driver.get(GOG_URL + searchTerm)

        time.sleep(1) # basic async handling for now

        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        gogGame = GameDetails()
        gogGame.store = "GOG"

        results = soup.find(class_ = "list-inner")

        if (results != None):
            res = results.find_all(class_ = "product-tile__content js-content")
            gogGame.gameTitle = res[0].find(class_ = "product-tile__title").string
            hasDiscount = res[0].find(class_ = "product-tile__discount")

            if (hasDiscount != None):
                originalPrice = res[0].find(class_ = "product-tile__price _price").string
                gogGame.originalPrice = "CDN$ " + str(originalPrice)
                discountedPrice = res[0].find(class_ = "product-tile__price-discounted _price").string
                gogGame.discountedPrice = "CDN$ " + str(discountedPrice)
                gogGame.discountPct = str(hasDiscount.string)
            else:
                originalPrice = res[0].find(class_ = "product-tile__price-discounted _price").string
                gogGame.originalPrice = "CDN$ " + str(originalPrice)

        driver.quit()
        return gogGame
    except Exception as error:
        print(error)
        return handleError("GOG")

def scrapeFanatical(searchTerm):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--incognito")
        options.add_argument("--log-level=3")
        driver = webdriver.Chrome(options = options)
        driver.get(FANATICAL_URL + searchTerm)

        time.sleep(1)

        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        fanaticalGame = GameDetails()
        fanaticalGame.store = "Fanatical"

        results = soup.find(class_ = "ais-Hits__root")

        if (results != None and results.contents):
            res = results.find_all(class_ = "card-container col-6 col-sm-4 col-md-6 col-lg-4")
            imgs = res[0].find_all("img")
            fanaticalGame.gameTitle = imgs[0].get("alt")
            hasDiscount = res[0].find(class_ = "card-saving")

            if (hasDiscount != None):
                originalPrice = res[0].find(class_ = "was-price").string
                fanaticalGame.originalPrice = "CDN$ " + str(originalPrice)[3:]
                discountedPrice = res[0].find(class_ = "card-price").string
                fanaticalGame.discountedPrice = "CDN$ " + str(discountedPrice)[3:]
                fanaticalGame.discountPct = str(hasDiscount.text)
            else:
                originalPrice = res[0].find(class_ = "card-price").string
                fanaticalGame.originalPrice = "CDN$ " + str(originalPrice)[3:]

        driver.quit()
        return fanaticalGame
    except Exception as error:
        print(error)
        return handleError("Fanatical")

# game = scrapeFanatical("children of morta")
# print(game.gameTitle)
# print(game.originalPrice)
# print(game.discountedPrice)
# print(game.discountPct)
