FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 7860 for Hugging Face Spaces
EXPOSE 7860

# Run FastAPI app with uvicorn, binding to port 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
