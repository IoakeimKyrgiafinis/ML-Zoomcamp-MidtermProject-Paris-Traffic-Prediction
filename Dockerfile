FROM python:3.12.8-slim

WORKDIR /app

# Install necessary python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model and prediction script into the container
COPY predict.py .
COPY model_paris_traffic.bin .

EXPOSE 9696

ENTRYPOINT ["python", "predict.py"]