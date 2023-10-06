#!/usr/bin/python3
"""a Fabric script (based on the file 1-pack_web_static.py),
that distributes an archive to your web servers,
using the function do_deploy"""

from fabric.api import env, run, put
from os.path import exists

env.user = 'ubuntu'
env.hosts = ['52.205.94.206', '52.86.161.51']


def do_deploy(archive_path):
    """Deploys a web static archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ on the web server
        put(archive_path, "/tmp/")

        # Extract the archive to the releases directory
        archive_filename = archive_path.split("/")[-1]
        archive_folder = "/data/web_static/releases/{}".format(
            archive_filename.split(".")[0])
        run("mkdir -p {}".format(archive_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, archive_folder))

        # Delete the archive from the server
        run("rm /tmp/{}".format(archive_filename))

        # Move files out of web_static subdirectory
        run("mv {}/web_static/* {}".format(archive_folder, archive_folder))

        # Remove the now empty web_static subdirectory
        run("rm -rf {}/web_static".format(archive_folder))

        # Remove the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(archive_folder))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed: {}".format(str(e)))
        return False
