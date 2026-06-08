FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY gui/ ./gui/
COPY scraper/ ./scraper/
COPY database/ ./database/
COPY templates/ ./templates/
WORKDIR /app/gui
CMD ["python", "app.py"]