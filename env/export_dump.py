#!/usr/bin/env python
# coding: utf-8

import datetime
import os

user = "root"
host = "127.0.0.1"
port = 3306
db = "auto_model_learning"


def most_recent_correct_dump(dump_names):
    copy_names = dump_names.copy()
    copy_names.reverse()
    most_recent_name = ''
    for name in copy_names:
        with open("./dumps/" + name, "r") as f:
            if '-- Dump completed' in f.read():
                most_recent_name = name
                break
    return most_recent_name


def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def try_to_read(command):
    connected = False
    for i in range(3):
        if len(os.popen(command).read()) > 0:
            connected = True
            break
    return connected


def update_most_recent(date):
    envs = []
    with open("../.env", "r") as f:
        envs = f.read().split()
    new_envs = replace_most_recent(envs, date)
    with open("../.env", "w+") as f:
        f.write(new_envs)


def replace_most_recent(envs, date):
    new_envs = []
    for env in envs:
        if "MOST_RECENT=" not in env:
            new_envs.append(env)
    new_envs.append(f'MOST_RECENT="{date}"')
    return f"{os.linesep}".join(new_envs)


def get_latest_log_date(path):
    with open(path, "r") as f:
        logs = f.read()
        logs_arr = logs.split(os.linesep)
        if len(logs_arr) > 1:
            latest = logs_arr[-2]
            date = latest.split()[0]
            return compare_date_with_today(date)
        return None


def compare_date_with_today(latest):
    today_date = datetime.datetime.now().date()
    latest_date = datetime.datetime.strptime(latest, "%Y-%m-%d").date()
    return (today_date - latest_date).days


def replace_log(path):
    latest_date = get_latest_log_date(path)
    if latest_date is not None and latest_date > 0:
        with open(path, "w") as f:
            f.write('')


path = f"{os.getcwd()}/dumps/"
today = datetime.datetime.now().strftime("%Y-%m-%d")
select_cmd = f'mariadb -h {host} -P {port} -u {user} -e "use auto_model_learning; show tables;"'
replace_log("./logs/dump_log.txt")
if try_to_read(select_cmd):
    path += f"{today}.sql"
    if os.path.exists(path):
        print(f"{get_time()} Database dump for {today} already exists")
    else:
        dump_cmd = f"mysqldump -h {host} -P {port} -u {user} {db} -B > {path}"
        os.popen(dump_cmd)
        print(f"{get_time()} Database dumped to {today}.sql")
        update_most_recent(today)
else:
    print(f'{get_time()} It seems db container is not running or there is no data inside. Check db container state '
          f'and mounted volumes')
    dump_names = os.popen("cd ./dumps; ls").read().split()
    most_correct_recent_name = most_recent_correct_dump(dump_names)
    if len(most_correct_recent_name) == 0:
        print(f'{get_time()} There are no correct dump files. Try to create it manually')
        path = ''
    else:
        path += f"{most_correct_recent_name}"
        date = most_correct_recent_name.split(".sql")[0]
        print(f"{get_time()} Database backuped to {date}.sql")
        update_most_recent(date)
