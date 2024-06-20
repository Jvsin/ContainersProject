FROM python

RUN mkdir -p /home/app

COPY . /home/app

RUN pip install -r /home/app/requirements.txt

CMD ["python", "/home/front/server.py"]

EXPOSE 4000