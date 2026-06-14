from flask import Flask, render_template, request
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "scraper"))
sys.path.append(str(Path(__file__).parent.parent / "database"))

from scraper import uruchom_scraper
from database import zapisz_wyniki, pobierz_wszystkie

app = Flask(__name__, template_folder="../templates")

@app.route("/")
def index():
    wyniki = pobierz_wszystkie()
    return render_template("index.html", wyniki=wyniki, komunikat=None)

@app.route("/scrape", methods=["POST"])
def scrape():
    urls_raw = request.form.get("urls", "")
    urls = [u.strip() for u in urls_raw.strip().splitlines() if u.strip()]

    if not urls:
        wyniki = pobierz_wszystkie()
        return render_template("index.html", wyniki=wyniki, komunikat="Nie podano żadnych adresów URL!")

    nowe = uruchom_scraper(urls)
    zapisz_wyniki(nowe)
    wyniki = pobierz_wszystkie()
    return render_template("index.html", wyniki=wyniki, komunikat=f"Scrapowanie zakończone! Pobrano dane z {len(nowe)} stron.")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
