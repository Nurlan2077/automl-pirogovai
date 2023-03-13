# automl-pirogovai

## Правила работы в репозитории
1.  Есть ветки ml, backend, frontend, которые соответствуют компонентам архитектуры.<br/>
1.1.  В ветке ml работают [Александр](https://github.com/aamochalov) и [Нурлан](https://github.com/Nurlan2077).<br/>
1.2.  В ветке backend работают [Мария](https://github.com/MSenso) и [Матвей](https://github.com/michigantsev).<br/>
1.3.  В ветке frontend работает Дарина.<br/>
2.  Все компоненты (ml, backend, frontend) развёртываются отдельно (микросервисная архитектура), общаются по API.<br/>
2.1.  Контракты по API предварительно обсуждаются обеими сторонами (ml и backend, backend и frontend).<br/>
2.2.  В readme каждой ветки будет инструкция по развертыванию компонента этой ветки.<br/>
3.  Для каждой единицы нового функционала создаётся отдельная ветка от базовой и сливается в базовую по готовности.<br/>
3.1.  В главных ветках (ml, backend, frontend) только рабочий оттестированный код, который локально могут развёртывать другие члены команды.<br/>


# Backend

Prefer to develop for Linux because of Docker issues on Windows.


What to install:

<code>pip install mariadb</code>

<code>pip install fastapi</code>

<code>sudo apt install uvicorn</code>

install MariaDB Community from there: https://mariadb.com/downloads/

install Docker and Docker Engine from there: https://docs.docker.com/engine/install/ubuntu/

How to run app: you shoud to use docker compose to launch both backend and DB.

Run <code>docker compose build</code> to build containers (make sure to do it after every change in code)

Run <code>docker compose up -d </code> to run DB and backend


Some useful commands:

<code>docker rm container_name [optional: -f]</code> - remove container. Use flag -f to remove used container

<code>docker rmi image_name </code> - remove docker image

<code>docker compose down [optional: -v] </code> - stop and remove containers and networks defined in docker-compose.yml. Use flag -v to remove volumes (i.e. attached DB dump)

<code>docker logs container_name [optional: -f] </code> - check logs of specific container. Use flag -f to do it in real-time

How to export a dump: <code>mysqldump -h 127.0.0.1 -P 3306 -u root auto_model_learning -B > path/to/env/dumps/YYYY-MM-DD.sql</code>

How to work with dumps: https://simplebackups.com/blog/the-complete-mysqldump-guide-with-examples/#importing-a-mysqldump