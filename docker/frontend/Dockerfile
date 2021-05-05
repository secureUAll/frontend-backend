FROM python:3
COPY secureuall/ /app
RUN  apt update -y
RUN apt install postgresql postgresql-contrib -y
RUN apt install xmlsec1 -y
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
