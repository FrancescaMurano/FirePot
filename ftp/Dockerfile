FROM python:3.8
WORKDIR /app
COPY . .

RUN pip3 install -r app/requirements.txt

CMD ["python3", "app/ftp_server.py"]

EXPOSE 21 2121 6000-6005
