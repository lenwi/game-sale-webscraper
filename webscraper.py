import requests
from bs4 import BeautifulSoup

steamUrl = "https://store.steampowered.com/search/?term="
winGameUrl = "https://www.wingamestore.com/search/?SearchWord="
GOGUrl = "https://www.gog.com/games?search="
humbleUrl = "https://www.humblebundle.com/store/search?sort=bestselling&search="

searchTerm = "children of morta"

steamPage = requests.get(steamUrl)

soup = BeautifulSoup(page.content, "html.parser")

print(soup)