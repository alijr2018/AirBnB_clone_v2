#!/usr/bin/python3
"""a Fabric script (based on the file 2-do_deploy_web_static.py),
that creates and distributes an archive to your web servers,
using the function deploy"""

from fabric.api import env, run, put, local
from os.path import exists
from datetime import datetime
from os import makedirs

env.user = 'ubuntu'
env.hosts = ['52.205.94.206', '52.86.161.51']


def do_pack():
    """ Generate a .tgz archive from the contents of the web_static folder. """
    try:
        if not exists("versions"):
            makedirs("versions")

        now = datetime.now()
        file_name = "web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))

        local("tar -cvzf versions/{} web_static".format(file_name))

        return "versions/{}".format(file_name)
    except Exception as e:
        return None


def do_deploy(archive_path):
    """ Distribute an archive to the web servers and deploy it.
    True if successful, False otherwise."""
    if not exists(archive_path):
        print("Archive not found.")
        return False

    try:
        put(archive_path, '/tmp/')

        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]
        release_path = "/data/web_static/releases/{}/".format(folder_name)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, release_path))

        run("rm /tmp/{}".format(file_name))

        run("mv {}web_static/* {}".format(release_path, release_path))
        run("rm -rf {}web_static".format(release_path))

        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed: {}".format(str(e)))
        return False


def deploy():
    archive_path = do_pack()

    if not archive_path:
        return False

    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
