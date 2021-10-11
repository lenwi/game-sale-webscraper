import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

STEAM_URL = 'https://store.steampowered.com/search/?term='
WINGAME_URL = 'https://www.wingamestore.com/search/?SearchWord='
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

def scrapegog(searchTerm):
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

    return gogGame