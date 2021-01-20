FROM python:3

WORKDIR /usr/src
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py *.sh ./

ENTRYPOINT [ "python" ]
CMD [ "./receive_events.py" ]
