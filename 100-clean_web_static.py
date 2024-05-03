#!/usr/bin/python3
# Fabric script that deletes out-of-date archives.
import os
from fabric.api import env, local, run

env.hosts = ["54.237.115.176", "54.234.13.131"]


def do_clean(number=0):
    """
    Delete out-of-date archives.

    Args:
        number (int): Number of archives to keep (including the most recent).

    Returns:
        bool: True if cleanup is successful, False otherwise.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
