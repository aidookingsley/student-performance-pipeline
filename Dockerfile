FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .


# Install packages
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for AWS credentials
ENV AWS_ACCESS_KEY_ID=your_access_key
ENV AWS_SECRET_ACCESS_KEY=your_secret_key
ENV AWS_DEFAULT_REGION=your_region

# Expose port 8501 for Streamlit
EXPOSE 8501


COPY . /app/

CMD [ "streamlit", "run", "app/app.py", "--server.port", "8501", "--server.address=0.0.0.0" ]