FROM python:3.7-alpine

COPY flask3.py /flask/
COPY trendstream4.py /flask/
COPY sqldata1.py /flask/
COPY myconfig.py /flask/
COPY templates /flask/templates
COPY static /flask/static
COPY requirements.txt /tmp
COPY test1.py /flask/
COPY test2.py /flask/
COPY server-debug.sh /flask/
COPY twitter_data.db /flask/

RUN pip3 install -r /tmp/requirements.txt

EXPOSE 5000

WORKDIR /flask
# CMD ["python3", "trendstream4.py"]
CMD ["python3", "flask3.py"]
