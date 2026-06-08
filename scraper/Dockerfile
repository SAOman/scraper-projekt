FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY scraper/ ./scraper/
WORKDIR /app/scraper
CMD ["python", "scraper.py"]