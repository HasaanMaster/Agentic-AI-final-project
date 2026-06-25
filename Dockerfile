FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (faster rebuilds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project (code + knowledge base + prebuilt search index)
COPY . .

# Cloud Run sends web traffic to $PORT (8080 by default).
ENV PORT=8080
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true