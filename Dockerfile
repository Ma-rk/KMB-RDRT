FROM python:3.12.5-slim-bookworm

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0", "--port=80" ]
