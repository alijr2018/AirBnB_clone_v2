#!/usr/bin/python3
"""a Fabric script (based on the file 1-pack_web_static.py),
that distributes an archive to your web servers,
using the function do_deploy"""

from fabric.api import env, run, put
from os.path import exists

env.user = 'ubuntu'
env.hosts = ['52.205.94.206', '52.86.161.51']


def do_deploy(archive_path):
    """ Distribute an archive to the web servers and deploy it.
    True if successful, False otherwise.
    """
    if not exists(archive_path):
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

        return True
    except Exception as e:
        return False


if __name__ == "__main__":

    do_deploy(archive_path)
