#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers using the function do_deploy.
"""


import os.path
from fabric.api import env, put, run

# Define the list of web server IPs and the SSH username
env.hosts = ["54.237.115.176", "54.234.13.131"]
env.user = "ubuntu"

def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path (str): Path of the archive to be deployed.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False

    try:
        file = os.path.basename(archive_path)
        name = os.path.splitext(file)[0]

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
    # Example usage
    archive_path = "your_archive_path_here"
    do_deploy(archive_path)

