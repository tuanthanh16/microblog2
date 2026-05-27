FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a volume for the SQLite database
VOLUME /app/data

ENV PORT=7000
EXPOSE $PORT

#MD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
#CMD ["python", "app.py"]
CMD exec flask run -h 0.0.0.0 -p 7000