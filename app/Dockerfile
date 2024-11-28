FROM python:3.11.7-slim-bookworm

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && \
    pip install --upgrade pip

COPY . .

# To set the locale for the time and date format
RUN locale-gen en_GB.UTF-8
# Set environment variables for locale
ENV LANG=en_GB.UTF-8
ENV LANGUAGE=en_GB:en

# To set the timezone
ENV TZ=Asia/Nicosia
RUN ln -fs /usr/share/zoneinfo/Asia/Nicosia /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Install necessary libraries
RUN pip install --no-cache-dir -r requirements.txt

# Clean it up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Make an alias
RUN echo '#!/bin/bash\npython app.py' > /usr/local/bin/go && \
    chmod +x /usr/local/bin/go

# Print messages to the Docker logs at container startup
CMD echo "You can use the alias \033[1;34m'go'\033[0m to run the Python script main.py." && \
    bash