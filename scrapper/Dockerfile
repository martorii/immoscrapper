FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt /
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt
COPY . .
CMD ["database/start_up.py", "fotocasa_scrap.py", "pisos_scrap.py"]
ENTRYPOINT ["python3"]