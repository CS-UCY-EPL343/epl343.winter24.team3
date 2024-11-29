FROM python:3.10-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && \
    pip install --upgrade pip

COPY . .

# # Set environment variables for locale
# ENV LANG=en_GB.UTF-8
# ENV LANGUAGE=en_GB:en

# # To set the timezone
# ENV TZ=Asia/Nicosia
# RUN ln -fs /usr/share/zoneinfo/Asia/Nicosia /etc/localtime && \
#     dpkg-reconfigure -f noninteractive tzdata

# Install necessary libraries
RUN pip install --no-cache-dir -r requirements.txt

# Clean it up
# RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose port 5000 to access the Flask application
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1

# Run the Flask app
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
