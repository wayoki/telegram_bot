FROM python:3.13-slim
WORKDIR /bot
RUN apt-get update && apt-get install -y iputils-ping
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "bot.py" ]
