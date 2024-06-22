FROM python

RUN mkdir -p /home/connection

COPY . /home/connection

RUN pip install -r /home/connection/requirements.txt

CMD ["python", "/home/connection/database.py"]

EXPOSE 4001