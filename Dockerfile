# Use official Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install OS dependencies (needed for building Python and Rust packages)
RUN apt-get update && \
    apt-get install -y build-essential curl git pkg-config libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Rust for maturin
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Set Rust to use writable directories inside /app
ENV PATH="/root/.cargo/bin:${PATH}"
ENV CARGO_HOME=/app/.cargo
ENV RUSTUP_HOME=/app/.rustup

# Copy only requirements first to leverage Docker caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the app (includes FastAPI code + static frontend)
COPY . .

# Expose the port Render will use
EXPOSE 8080

# Run FastAPI using Render's dynamic port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
