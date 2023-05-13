FROM python:3.10

WORKDIR /auto_post

COPY . /auto_post

RUN pip install -r requirements.txt

CMD ["python", "main.py"]