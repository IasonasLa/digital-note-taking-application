FROM kalilinux/kali-rolling
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install flask pymongo
RUN mkdir  /app
COPY gg.py /app/gg.py
EXPOSE 5000
WORKDIR /app
ENTRYPOINT ["python3","-u","gg.py"]
