FROM python:3.10.9-bullseye

RUN apt-get update && \
  apt-get install -y apt-transport-https curl && \
  curl -o /etc/apt/trusted.gpg.d/mariadb_release_signing_key.asc 'https://mariadb.org/mariadb_release_signing_key.asc' && \
  sh -c "echo 'deb https://mirrors.ircam.fr/pub/mariadb/repo/10.10/debian bullseye main' >>/etc/apt/sources.list" && \
  apt-get update && \
  apt-get install -y libmariadb3 libmariadb-dev unrar-free && \
  rm -rf /var/cache/apt

WORKDIR app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
