#!/usr/bin/env python
# coding: utf-8

import os


def most_recent_correct_dump(dump_names):
    copy_names = dump_names.copy()
    copy_names.reverse()
    most_recent_name = ''
    for name in copy_names:
        with open("./dumps/"+name, "r") as f:
            if '-- Dump completed' in f.read():
                most_recent_name = name
                break
    return most_recent_name


def remove_files(dumps, most_recent_name):
    for name in dumps:
        if name != most_recent_name:
            os.remove(f"./dumps/{name}")


dumps = os.popen("cd ./dumps; ls").read().split()
name = most_recent_correct_dump(dumps)
remove_files(dumps, m)

