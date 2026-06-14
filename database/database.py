from pymongo import MongoClient
import os

def polacz():
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(MONGO_URI)
    db = client["scraper_db"]
    return db

def zapisz_wyniki(wyniki):
    db = polacz()
    kolekcja = db["data"]
    nowe = 0
    for wynik in wyniki:
        istnieje = kolekcja.find_one({"url": wynik["url"]})
        if not istnieje:
            kolekcja.insert_one(wynik)
            nowe += 1
        else:
            # Aktualizuj istniejący rekord
            kolekcja.replace_one({"url": wynik["url"]}, wynik)
    print(f"Zapisano/zaktualizowano {len(wyniki)} rekordów")

def pobierz_wszystkie():
    db = polacz()
    return list(db["data"].find({}, {"_id": 0}))
