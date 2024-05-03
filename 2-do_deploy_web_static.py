#!/usr/bin/python3
"""
A scrpt that distributes an archive to web servers using the function.
"""
from fabric.api import env, put, run
from os.path import exists
import os


# Define the list of web server IPs
env.hosts = ['54.237.115.176', '54.234.13.131']
# Define the SSH username
env.user = 'ubuntu'

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
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')
        archive_name = archive_path.split('/')[-1]
        release_path = '/data/web_static/releases/' + archive_name[:-4]
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, release_path))
        run('rm /tmp/{}'.format(archive_name))
        run('mv {}/web_static/* {}'.format(release_path, release_path))
        run('rm -rf {}/web_static'.format(release_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_path))
        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    do_deploy(archive_path)
