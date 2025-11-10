FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*
# C++ compilers are required to build some Python packages WAOW

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY my_agent/ ./my_agent/

RUN mkdir -p ./backend/uploads
# Just to be sure the folder exists

ENV PYTHONPATH=/app
# Change later if needed


EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
