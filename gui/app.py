from flask import Flask, render_template, request
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "scraper"))
sys.path.append(str(Path(__file__).parent.parent / "database"))

from scraper import uruchom_scraper
from database import zapisz_cytaty, pobierz_wszystkie

app = Flask(__name__, template_folder="../templates")

@app.route("/")
def index():
    cytaty = pobierz_wszystkie()
    return render_template("index.html", cytaty=cytaty, komunikat=None)

@app.route("/scrape", methods=["POST"])
def scrape():
    ile = int(request.form.get("ile_stron", 10))
    nowe = uruchom_scraper(ile_stron=ile)
    zapisz_cytaty(nowe)
    cytaty = pobierz_wszystkie()
    return render_template("index.html", cytaty=cytaty, komunikat=f"Pobrano i zapisano {len(nowe)} cytatów!")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)