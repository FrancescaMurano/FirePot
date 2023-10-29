FROM python:3.8
WORKDIR /app
COPY . .

RUN pip3 install -r app/requirements.txt

CMD ["python3", "app/honeyssh.py"]

EXPOSE 8083 22 23
