FROM python:3.10.3-slim-bullseye

LABEL maintainer="https://suk.kr"

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY . .

# RUN apt-get -y update
# RUN apt-get install -y --fix-missing \
#     build-essential \
#     cmake \
#     gfortran \
#     git \
#     wget \
#     curl \
#     graphicsmagick \
#     libgraphicsmagick1-dev \
#     libatlas-base-dev \
#     libavcodec-dev \
#     libavformat-dev \
#     libgtk2.0-dev \
#     libjpeg-dev \
#     liblapack-dev \
#     libswscale-dev \
#     pkg-config \
#     python3-dev \
#     python3-numpy \
#     software-properties-common \
#     zip \
#     && apt-get clean && rm -rf /tmp/* /var/tmp/*

# RUN cd ~ && \
#     mkdir -p dlib && \
#     git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
#     cd  dlib/ && \
#     python3 setup.py install --yes USE_AVX_INSTRUCTIONS

RUN apt update
RUN apt install -y build-essential cmake wget git libxrender1 fonts-nanum fontconfig libgl1-mesa-glx libglib2.0-0
RUN pip install fastapi uvicorn requests openai pdfkit python-dotenv opencv-python python-multipart cmake
RUN fc-cache -fv

WORKDIR /app/dlib
RUN python /app/dlib/setup.py install

RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
RUN tar vxf wkhtmltox-0.12.3_linux-generic-amd64.tar.xz 
RUN cp wkhtmltox/bin/wk* /usr/local/bin/

WORKDIR /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]