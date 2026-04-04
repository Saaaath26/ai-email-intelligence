FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn openai

EXPOSE 8000

CMD ["python", "inference.py"]