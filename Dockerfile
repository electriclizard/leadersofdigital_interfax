FROM python:3.9
WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install -U pip
RUN pip install -U setuptools
RUN pip install -r requirements.txt

COPY . ./
ENTRYPOINT [ "python", "./app.py" ]