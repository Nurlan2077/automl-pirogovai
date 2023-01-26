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

<code>mariadb -h 127.0.0.1 -P 3306 -u root</code> - enter command line MariaDB interface

<code>mysqldump -h 127.0.0.1 -P 3306 -u root auto_model_learning -B > path/to/env/dumps/YYYY-MM-DD.sql</code> - export db dump manually (in case scheduler is not working or if you need a new dump right now). Also make sure to update MOST_RECENT variable in .env file so it points to the dump you need

How to work with dumps: https://simplebackups.com/blog/the-complete-mysqldump-guide-with-examples/#importing-a-mysqldump
