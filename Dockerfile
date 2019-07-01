FROM python:3.6-slim-stretch

#RUN apt-get -y update \
#    && apt-get install -y --no-install-recommends

RUN python3 -m pip install lxml
RUN python3 -m pip install pandas
RUN python3 -m pip install PyYAML
RUN python3 -m pip install requests
RUN python3 -m pip install tqdm

RUN mkdir -p /opt/program

WORKDIR /opt/program
COPY main.py /opt/program
COPY src/ /opt/program/src
COPY data/ /opt/program/data

CMD [ "python", "./main.py" ]
