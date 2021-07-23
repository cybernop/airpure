FROM python:3.9
WORKDIR /app
RUN apt update && apt install git
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT [ "python", "main.py" ]
