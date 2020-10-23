FROM ubuntu:18.04

RUN apt-get update ; apt-get install -y git build-essential gcc make yasm autoconf automake cmake libtool checkinstall libmp3lame-dev pkg-config libunwind-dev zlib1g-dev libssl-dev

RUN apt-get update \
    && apt-get clean \
    && apt-get install -y --no-install-recommends libc6-dev libgdiplus wget software-properties-common python3-pip

RUN wget https://www.ffmpeg.org/releases/ffmpeg-4.3.1.tar.gz
RUN tar -xzf ffmpeg-4.3.1.tar.gz; rm -r ffmpeg-4.3.1.tar.gz
RUN cd ./ffmpeg-4.3.1; ./configure --enable-gpl --enable-libmp3lame --enable-decoder=mjpeg,png --enable-encoder=png --enable-openssl --enable-nonfree

RUN cd ./ffmpeg-4.3.1; make
RUN  cd ./ffmpeg-4.3.1; make install

COPY . /app

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "bot.py"]