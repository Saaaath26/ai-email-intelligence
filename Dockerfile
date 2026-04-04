FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn

EXPOSE 8000

# 🔥 FORCE inference.py ONLY
CMD ["python", "-m", "uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8000"]