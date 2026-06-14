# 🌐 Web Scraper

Projekt semestralny — Przetwarzanie równoległe i rozproszone  
ANS w Elblągu, Instytut Informatyki Stosowanej

**Autor:** Szymon Oman 21519
**Grupa:** 2  
**Repozytorium:** https://github.com/SAOman/scraper-projekt

---

## Opis projektu

Aplikacja do automatycznego pobierania, przetwarzania i przechowywania danych ze stron internetowych w architekturze rozproszonej.

Użytkownik podaje adresy URL przez interfejs webowy. System pobiera dane **asynchronicznie** (asyncio + aiohttp), przetwarza je **równolegle** (multiprocessing) i zapisuje w bazie **MongoDB**.

### Pobierane grupy danych:
- 📧 Adresy e-mail
- 📞 Numery telefonów
- 🔗 Linki (href)
- 📰 Nagłówki H1 i H2
- Tytuł strony i opis meta

---

## Architektura

```
[ GUI - Flask ]  →  [ Scraper - Python ]  →  [ MongoDB ]
   port 5000           wewnętrzny              port 27017
```

Każdy moduł działa jako osobny kontener Docker.

---

## Technologie

| Technologia | Zastosowanie |
|---|---|
| Python | Język programowania |
| Flask | Interfejs webowy |
| asyncio + aiohttp | Asynchroniczne pobieranie stron |
| multiprocessing | Równoległe przetwarzanie (4 procesy) |
| BeautifulSoup4 | Parsowanie HTML |
| MongoDB + pymongo | Baza danych NoSQL |
| Docker + Docker Compose | Konteneryzacja 3 modułów |

---

## Uruchomienie (Docker)

```bash
git clone https://github.com/SAOman/scraper-projekt.git
cd scraper-projekt
docker-compose up --build
```

Aplikacja dostępna pod adresem: **http://localhost:5000**

Zatrzymanie:
```bash
docker-compose down
```

---

## Uruchomienie lokalne

```bash
# 1. Klonowanie
git clone https://github.com/SAOman/scraper-projekt.git
cd scraper-projekt

# 2. Środowisko wirtualne
python -m venv .venv
.venv\Scripts\activate

# 3. Zależności
pip install -r requirements.txt

# 4. Uruchomienie MongoDB
mongod --dbpath C:\data\db

# 5. Uruchomienie silnika i interfejsu
cd scraper
python scraper.py

cd ../gui
python app.py
```

---

## Jak używać

1. Otwórz http://localhost:5000
2. Wklej adresy URL w polu tekstowym (każdy w nowej linii), np.:
```
https://www.wp.pl
https://www.python.org
https://www.mongodb.com/contact
```
3. Kliknij **Start Scrapowania**
4. Wyniki pojawią się na stronie i zostaną zapisane w MongoDB (`scraper_db` → `data`)

---

## Struktura projektu

```
scraper-projekt/
├── scraper/
│   ├── scraper.py        # Silnik scrapujący (asyncio + multiprocessing)
│   └── Dockerfile
├── gui/
│   ├── app.py            # Interfejs Flask
│   └── Dockerfile
├── database/
│   └── database.py       # Połączenie z MongoDB
├── templates/
│   └── index.html        # Szablon HTML
├── requirements.txt
└── docker-compose.yml
```