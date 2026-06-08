import requests
from bs4 import BeautifulSoup
import multiprocessing
import asyncio
import aiohttp

BASE_URL = "https://quotes.toscrape.com/page/{}/"

# Zbieramy 4 grupy danych z każdego cytatu:
# 1. treść cytatu
# 2. autor
# 3. tagi
# 4. link do profilu autora

def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    quotes = []
    for q in soup.select(".quote"):
        tekst = q.select_one(".text").get_text(strip=True)
        autor = q.select_one(".author").get_text(strip=True)
        tagi = [t.get_text(strip=True) for t in q.select(".tag")]
        link_autora = "https://quotes.toscrape.com" + q.select_one("a")["href"]
        quotes.append({
            "tekst": tekst,
            "autor": autor,
            "tagi": tagi,
            "link_autora": link_autora
        })
    return quotes

async def pobierz_strone(session, numer):
    url = BASE_URL.format(numer)
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text()
        return None

async def pobierz_wszystkie_strony(numery):
    async with aiohttp.ClientSession() as session:
        zadania = [pobierz_strone(session, n) for n in numery]
        return await asyncio.gather(*zadania)

def scrape_zakres(numery):
    htmle = asyncio.run(pobierz_wszystkie_strony(numery))
    wyniki = []
    for html in htmle:
        if html:
            wyniki.extend(parse_page(html))
    return wyniki

def uruchom_scraper(ile_stron=10):
    # Dzielimy strony na 4 procesy
    wszystkie = list(range(1, ile_stron + 1))
    podzial = [wszystkie[i::4] for i in range(4)]

    with multiprocessing.Pool(processes=4) as pool:
        wyniki_czesciowe = pool.map(scrape_zakres, podzial)

    wszystkie_cytaty = []
    for czesc in wyniki_czesciowe:
        wszystkie_cytaty.extend(czesc)

    print(f"Pobrano {len(wszystkie_cytaty)} cytatów")
    return wszystkie_cytaty

if __name__ == "__main__":
    dane = uruchom_scraper()
    for d in dane[:3]:
        print(d)