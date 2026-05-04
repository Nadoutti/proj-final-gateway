FROM python:3.12-slim

WORKDIR /app

RUN addgroup --system app && adduser --system --group app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R app:app /app
USER app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
