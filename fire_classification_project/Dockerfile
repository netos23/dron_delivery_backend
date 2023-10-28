FROM nvidia/cuda:12.2.2-base-ubuntu22.04
RUN apt-get -y update \
    && apt-get install -y software-properties-common \
    && apt-get -y update

RUN apt-get -y install ffmpeg libsm6 libxext6
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN pip3 install --upgrade pip setuptools wheel
COPY ./app.py /app/app.py
COPY ./model.h5 /app/model.h5
COPY ./train.py /app/train.py
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]