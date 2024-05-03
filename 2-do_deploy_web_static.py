#!/usr/bin/python3
"""
Fabric of an archive to your web servers using the function do_deploy.
"""


from fabric.api import env, put, run
from os.path import exists
import os

env.hosts = ["54.237.115.176", "54.234.13.131"]

def do_deploy(archive_path):
    """
    Distribute an archive to the web servers.

    Args:
        archive_path (str): Path to the archive to be deployed.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        file = archive_path.split("/")[-1]
        name = file.split(".")[0]

        put(archive_path, "/tmp/{}".format(file))
        run("rm -rf /data/web_static/releases/{}/".format(name))
        run("mkdir -p /data/web_static/releases/{}/".format(name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name))
        run("rm /tmp/{}".format(file))
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))

        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    do_deploy(archive_path)

