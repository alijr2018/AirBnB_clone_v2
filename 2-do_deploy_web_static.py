#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, run, put
from os.path import exists

env.hosts = ['52.205.94.206', '52.86.161.51']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Deploys a web static archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ on the web server
        put(archive_path, "/tmp/")
        archive_filename = archive_path.split("/")[-1]
        archive_folder = "/data/web_static/releases/{}".format(
            archive_filename.split(".")[0])

        # Extract the archive to the releases directory
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
