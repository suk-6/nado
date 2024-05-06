FROM python:3.10.3-slim-bullseye

LABEL maintainer="https://suk.kr"

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY . .

RUN apt update
RUN apt install -y build-essential cmake wget git libxrender1 fonts-nanum fontconfig libgl1-mesa-glx libglib2.0-0 libssl1.0-dev
RUN pip install fastapi uvicorn requests openai pdfkit python-dotenv opencv-python python-multipart cmake
RUN fc-cache -fv

WORKDIR /app/dlib
RUN git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git /app/dlib
RUN python /app/dlib/setup.py install

RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
RUN tar vxf wkhtmltox-0.12.3_linux-generic-amd64.tar.xz 
RUN cp wkhtmltox/bin/wk* /usr/local/bin/

WORKDIR /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]