from pymongo import MongoClient

def polacz():
    import os
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(MONGO_URI)
    db = client["scraper_db"]
    return db

def zapisz_cytaty(cytaty):
    db = polacz()
    kolekcja = db["cytaty"]
    nowe = 0
    for cytat in cytaty:
        istnieje = kolekcja.find_one({"tekst": cytat["tekst"]})
        if not istnieje:
            kolekcja.insert_one(cytat)
            nowe += 1
    print(f"Zapisano {nowe} nowych cytatów (duplikaty pominięte)")

def pobierz_wszystkie():
    db = polacz()
    return list(db["cytaty"].find({}, {"_id": 0}))

if __name__ == "__main__":
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).parent.parent / "scraper"))
    from scraper import uruchom_scraper
    cytaty = uruchom_scraper()
    zapisz_cytaty(cytaty)
    print("Przykładowe rekordy z bazy:")
    for c in pobierz_wszystkie()[:2]:
        print(c)