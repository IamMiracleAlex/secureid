FROM python:3.8.8-alpine


# RUN apk update \
#     && apk add gcc python3-dev musl-dev openssl-dev 
# RUN apk update \
#     && apk add gcc python3-dev musl-dev libffi-dev openssl-dev cargo

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

WORKDIR /

