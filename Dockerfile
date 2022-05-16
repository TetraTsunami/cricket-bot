# syntax=docker/dockerfile:1

# Grab Python, make a directory to store everything
FROM python:3.10-slim
WORKDIR /app

# Grab requirements
RUN apt-get update && apt-get install -y git
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Grab everything else
COPY . .

# Get inside
ENTRYPOINT ["python3"]
CMD ["-u", "bot.py"]