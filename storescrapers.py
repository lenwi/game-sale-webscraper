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

def create_driver():
    # chromium headless webdriver to get js content
    options = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}') # Bypass pages that don't allow headless
    options.add_argument("--headless")
    options.add_argument("--incognito")
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # hides devlogs from console
    driver = webdriver.Chrome(options = options)

    return driver

def scrapeSteam(searchTerm):
    print("Checking Steam...")
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
        
        print("Done!")

        return steamGame
    except Exception as error:
        print(error)
        return handleError("Steam")

def scrapegog(searchTerm):
    print("Checking GOG...")
    try:
        driver = create_driver()
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
        print("Done!")

        return gogGame
    except Exception as error:
        print(error)
        return handleError("GOG")

def scrapeFanatical(searchTerm):
    print("Checking Fanatical...")
    try:
        driver = create_driver()
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
        print("Done!")

        return fanaticalGame
    except Exception as error:
        print(error)
        return handleError("Fanatical")

def scrapeHumble(searchTerm):
    print("Checking Humble Bundle...")
    try:
        driver = create_driver()
        driver.get(HUMBLE_URL + searchTerm)

        time.sleep(1)

        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        humbleGame = GameDetails()
        humbleGame.store = "Humble Bundle"

        results = soup.find(class_ = "entities-list js-entities-list no-style-list full js-full")

        if (results != None and len(results.contents) >= 3):
            res = results.find_all(class_ = "entity-block-container js-entity-container")
            humbleGame.gameTitle = res[0].find(class_ = "entity-title").string
            hasDiscount = res[0].find(class_ = "js-discount-amount discount-amount")

            if (hasDiscount != None):
                originalPrice = res[0].find(class_ = "breakdown-full-price").string
                humbleGame.originalPrice = "CDN$ " + str(originalPrice)[3:]
                discountedPrice = res[0].find(class_ = "store-discounted-price").string
                humbleGame.discountedPrice = "CDN$ " + str(discountedPrice)[3:]
                humbleGame.discountPct = str(hasDiscount.text)[:-4].strip()
            else:
                originalPrice = res[0].find(class_ = "price").string
                humbleGame.originalPrice = "CDN$ " + str(originalPrice)[3:]

        driver.quit()
        print("Done!")
        
        return humbleGame
    except Exception as error:
        print(error)
        return handleError("humbleGame")