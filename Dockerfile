# Use official Python slim image
FROM python:3.12-slim

# OS dependencies
RUN apt-get update && \
    apt-get install -y build-essential curl git pkg-config libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Rust for maturin
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

# Use Render's dynamic PORT
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
