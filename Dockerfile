FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run uvicorn bound to 0.0.0.0 and the dynamically assigned $PORT
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
