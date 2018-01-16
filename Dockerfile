FROM python:rc-slim

RUN pip install bottle
RUN pip install pymongo
RUN pip install dnspython

ADD src src
CMD ["/usr/local/bin/python", "/src/server.py"]
