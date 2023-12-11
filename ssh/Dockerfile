FROM python:3.8
WORKDIR /app
COPY . .

RUN pip3 install -r app/requirements.txt

CMD ["python3", "app/honey_async_ssh.py"]

EXPOSE 2222 22 
