FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r ./server/requirements.txt

RUN python3 -m spacy download en_core_web_sm

RUN python3 db-init.py

EXPOSE 5000

CMD [ "python3", "./server/server.py" ]
