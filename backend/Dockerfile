FROM tensorflow/tensorflow:2.11.0-gpu

RUN apt-get update && \
  apt-get install -y software-properties-common
RUN curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && \
  apt-get install -y python3-setuptools libmariadb3 libmariadb-dev unrar python3.10 python3.10-dev python3.10-venv && \
  apt-get purge -y python3-pip && \
  rm -rf /var/cache/apt

WORKDIR app
RUN update-alternatives --install /usr/bin/python3 python /usr/bin/python3.8 1 && \
    update-alternatives --install /usr/bin/python3 python /usr/bin/python3.10 2 && \
    update-alternatives --config python


RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 # https://stackoverflow.com/questions/70431655/importerror-cannot-import-name-html5lib-from-pip-vendor-usr-lib-python3
RUN pip install tensorflow
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
