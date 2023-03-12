FROM ubuntu

WORKDIR /app

COPY requirements/ requirements/
run apt update && apt -y upgrade
run apt -y install git python3 python3-pip python3-dotenv
run pip3 install -r requirements/all.txt

COPY . .

CMD ["python3", "main.py"]
