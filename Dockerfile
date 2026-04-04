FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn openai pydantic

EXPOSE 8000

CMD ["sh", "-c", "python run_inference.py & uvicorn inference:app --host 0.0.0.0 --port 8000"]