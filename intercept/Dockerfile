FROM python:3.12.4-alpine

WORKDIR /intercept

COPY . /intercept

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]