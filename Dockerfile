# Dockerfile -- a blueprint for building images, 
# Image -- a template for running containers   (docker build -t space-game-img .) 
# Container -- the running procces (docker run -it --rm -e DISPLAY=unix$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --device /dev/snd space-game-img)

FROM python:3.10.6

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update && apt-get -y install --no-install-recommends \
    libfreetype6-dev \
    libportmidi-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    && rm -rf /var/lib/apt/lists  && pip install --no-cache-dir -r requirements.txt 

COPY . .

CMD [ "python", "app/Main.py" ]