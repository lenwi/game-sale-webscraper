from storescrapers import *

def displayInfo(arr):
    STORE = "{txt:^18}".format(txt = "Store")
    GAME_TITLE = "{txt:^50}".format(txt = "Game Title")
    ORIGINAL_PRICE = "{txt:^20}".format(txt = "Original Price")
    DISCOUNTED_PRICE = "{txt:^20}".format(txt = "Discounted Price")
    DISCOUNT_PERCENT = "{txt:^20}".format(txt = "Discount Percent")
    print("\n")
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

def get_games():
    steamGame = scrapeSteam(searchTerm)
    gogGame = scrapegog(searchTerm)
    fanaticalGame = scrapeFanatical(searchTerm)
    humbleGame = scrapeHumble(searchTerm)

    games = []
    games.append(steamGame)
    games.append(gogGame)
    games.append(fanaticalGame)
    games.append(humbleGame)

    return games

# Program start
print("\n\nEnter the name of a game:")
stringInput = input()
searchTerm = stringInput.lower()
print("\n")

games = get_games()

displayInfo(games)
