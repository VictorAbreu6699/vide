FROM python:3.11-slim


RUN apt-get update && \
    apt-get install -y --no-install-recommends pkg-config

RUN apt-get install -y python3-dev build-essential
RUN apt-get install -y default-libmysqlclient-dev


RUN apt-get install -y locales && \
    sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=pt_BR.UTF-8

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade -r  /app/requirements.txt

COPY src /src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7878","--reload"]