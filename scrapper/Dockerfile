FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt /
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt
COPY . .
CMD ["main.py"]
ENTRYPOINT ["python3"]