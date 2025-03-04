FROM python:3.11-alpine
RUN pip install --upgrade pip
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bot.py .
CMD ["python3", "bot.py"]
