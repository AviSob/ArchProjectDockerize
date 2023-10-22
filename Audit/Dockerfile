FROM ubuntu:22.04
LABEL maintainer = "asoboleva@my.bcit.ca"
RUN apt-get update -y && \
apt-get install -y python3 python3-pip && \
pip3 install -U flask
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app
EXPOSE 8110
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
