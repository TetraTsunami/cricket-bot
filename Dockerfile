# syntax=docker/dockerfile:1

# Grab Python, make a directory to store everything
FROM python:3.8
WORKDIR /app

# Grab requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Grab everything else
COPY . .

# Get inside
ENTRYPOINT ["python3"]
CMD ["-u", "bot.py"]