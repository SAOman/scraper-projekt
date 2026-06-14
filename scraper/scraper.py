import asyncio
import aiohttp
import multiprocessing
from bs4 import BeautifulSoup
import re

# Zbieramy 4+ grup danych z każdej strony:
# 1. Adresy e-mail
# 2. Numery telefonów
# 3. Linki (href)
# 4. Nagłówki H1/H2
# + tytuł strony, opis meta

def parse_page(html, url):
    soup = BeautifulSoup(html, "html.parser")

    # 1. Tytuł
    title = soup.title.get_text(strip=True) if soup.title else ""

    # 2. Adresy e-mail
    emails = list(set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", html)))

    # 3. Numery telefonów
    phones = list(set(re.findall(r"[\+]?[\d\s\-\(\)]{7,20}", html)))
    phones = [p.strip() for p in phones if len(p.strip()) >= 7]

    # 4. Linki
    links = list(set([
        a["href"] for a in soup.find_all("a", href=True)
        if a["href"].startswith("http")
    ]))

    # 5. Nagłówki H1
    headers = [h.get_text(strip=True) for h in soup.find_all("h1")]

    # 6. Nagłówki H2
    subheaders = [h.get_text(strip=True) for h in soup.find_all("h2")]

    # 7. Opis meta
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"] if desc_tag and desc_tag.get("content") else ""

    return {
        "url": url,
        "title": title,
        "emails": emails,
        "phones": phones,
        "links": links,
        "headers": headers,
        "subheaders": subheaders,
        "description": description
    }

async def pobierz_strone(session, url):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as response:
            if response.status == 200:
                html = await response.text()
                return html, url
    except Exception as e:
        print(f"Błąd pobierania {url}: {e}")
    return None, url

async def pobierz_wszystkie(urls):
    async with aiohttp.ClientSession() as session:
        zadania = [pobierz_strone(session, url) for url in urls]
        return await asyncio.gather(*zadania)

def scrape_zakres(urls):
    wyniki = []
    pary = asyncio.run(pobierz_wszystkie(urls))
    for html, url in pary:
        if html:
            wyniki.append(parse_page(html, url))
    return wyniki

def uruchom_scraper(urls):
    if not urls:
        return []

    # Dzielimy URLe na max 4 procesy
    n = min(4, len(urls))
    podzial = [urls[i::n] for i in range(n)]

    with multiprocessing.Pool(processes=n) as pool:
        wyniki_czesciowe = pool.map(scrape_zakres, podzial)

    wszystkie = []
    for czesc in wyniki_czesciowe:
        wszystkie.extend(czesc)

    print(f"Pobrano dane z {len(wszystkie)} stron")
    return wszystkie

if __name__ == "__main__":
    test_urls = ["https://www.wp.pl", "https://www.python.org"]
    dane = uruchom_scraper(test_urls)
    for d in dane:
        print(d["title"], "-", len(d["links"]), "linków")
