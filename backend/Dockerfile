FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

RUN apt-get update && \
  apt-get install -y libmariadb3 libmariadb-dev unrar python3.10 python3-pip && \
  rm -rf /var/cache/apt

WORKDIR app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
