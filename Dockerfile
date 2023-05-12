FROM ubuntu

WORKDIR /app

COPY requirements.txt requirements.txt
run apt update && apt -y upgrade
run apt -y install git python3 python3-pip python3-dotenv
run python3 -m pip install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
