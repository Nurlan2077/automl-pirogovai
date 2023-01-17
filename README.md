Prefer to develop for Linux because of Docker issues on Windows.


What to install:

<code>pip install mariadb</code>

<code>pip install fastapi</code>

<code>sudo apt install uvicorn</code>

install MariaDB Community from there: https://mariadb.com/downloads/

install Docker and Docker Engine from there: https://docs.docker.com/engine/install/ubuntu/

How to run:

- app: <code>python3 main.py</code>
- docker-compose: <code>docker compose up -d</code> in /env folder
- DB: <code>mariadb -h 127.0.0.1 -P 3306 -u root</code>

How to export a dump: mysqldump -h 127.0.0.1 -P 3306 -u root auto_model_learning -B > path/to/env/dumps/YYYY-MM-DD.sql

How to work with dumps: https://simplebackups.com/blog/the-complete-mysqldump-guide-with-examples/#importing-a-mysqldump
