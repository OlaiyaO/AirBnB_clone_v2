#!/usr/bin/python3
"""
A Fabric script that distributess an archive to my web servers.
"""
from datetime import datetime
from fabric.api import *
import os

env.hosts = ["54.237.115.176", "54.234.13.131"]
env.user = "ubuntu"

# Change the variable to specify the directory where the archive will be
ARCHIVE_DIR = "versions"


def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder.

    Returns:
        str: The path to the generated archive if successful, None otherwise.
    """
    local("mkdir -p {}".format(ARCHIVE_DIR))
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(date)
    archive_path = "{}/{}".format(ARCHIVE_DIR, archive_name)
    result = local(
            "tar -cvzf {} web_static".format(archive_path), capture=True
            )
    if result.succeeded:
        print("Packing successful!")
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """
    Distribute the .tgz archive to web servers.

    Args:
        archive_path (str): The path to the .tgz archive to deploy.

    Returns:
        bool: True if deployment was successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    remote_archive_path = "/tmp/{}".format(os.path.basename(archive_path))
    put(archive_path, "/tmp/")
    archive_name = os.path.basename(archive_path).split('.')[0]
    release_path = "/data/web_static/releases/{}/".format(archive_name)
    run("sudo mkdir -p {}".format(release_path))
    run("sudo tar -xzf {} -C {}".format(remote_archive_path, release_path))
    run("sudo rm {}".format(remote_archive_path))
    run("sudo mv {}web_static/* {}".format(release_path, release_path))
    run("sudo rm -rf {}web_static".format(release_path))
    run("sudo rm -rf /data/web_static/current")
    run("sudo ln -s {} /data/web_static/current".format(release_path))

    print("New version deployed!")
    return True
