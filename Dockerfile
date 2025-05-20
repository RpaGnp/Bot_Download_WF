FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1
ENV PATH="/scripts:${PATH}"

# Set timezone
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/America/Bogota /etc/localtime && \
    echo "America/Bogota" > /etc/timezone && \
    apk del tzdata

# Install system dependencies
RUN apk add --update --no-cache \
    bash \
    chromium \
    chromium-chromedriver \
    dos2unix \
    libxslt \
    openblas \
    libstdc++

# Install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create app directory
WORKDIR /app

# Copy application files
COPY ./app /app
COPY ./scripts /scripts

# Set permissions and convert line endings
RUN chmod +x /scripts/* && \
    dos2unix /scripts/*

# Set up cron
RUN crontab /scripts/crontab.txt

# Set entrypoint
ENTRYPOINT ["/scripts/entrypoint.sh"]