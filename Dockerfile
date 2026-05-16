FROM python:3.13-slim

WORKDIR /work
ENV HOST=0.0.0.0
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
COPY tools tools

EXPOSE 8086 8090
CMD ["python", "app/main.py"]
