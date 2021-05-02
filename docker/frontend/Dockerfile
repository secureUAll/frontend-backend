FROM python:3.8.9
COPY secureuall/ /app
ADD docker/frontend/entrypoint.sh /app
RUN  apt update -y
RUN apt install postgresql postgresql-contrib -y
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
