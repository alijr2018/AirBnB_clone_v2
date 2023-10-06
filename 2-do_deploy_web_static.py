#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, run, put
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Deploys a web static archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        print("[{}] Executing task 'do_deploy'".format(env.host))
        print("[{}] put: {} -> /tmp/{}".format(env.host, archive_path, archive_path.split("/")[-1]))

        # Upload the archive to /tmp/ on the web server
        put(archive_path, "/tmp/")

        # Extract the archive to the releases directory
        archive_filename = archive_path.split("/")[-1]
        archive_folder = "/data/web_static/releases/{}".format(
            archive_filename.split(".")[0])
        print("[{}] run: mkdir -p {}".format(env.host, archive_folder))
        run("mkdir -p {}".format(archive_folder))
        print("[{}] run: tar -xzf /tmp/{} -C {}".format(env.host, archive_filename, archive_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, archive_folder))

        # Delete the archive from the server
        print("[{}] run: rm /tmp/{}".format(env.host, archive_filename))
        run("rm /tmp/{}".format(archive_filename))

        # Move files out of web_static subdirectory
        print("[{}] run: mv {}/web_static/* {}".format(env.host, archive_folder, archive_folder))
        run("mv {}/web_static/* {}".format(archive_folder, archive_folder))

        # Remove the now empty web_static subdirectory
        print("[{}] run: rm -rf {}/web_static".format(env.host, archive_folder))
        run("rm -rf {}/web_static".format(archive_folder))

        # Remove the existing symbolic link
        print("[{}] run: rm -rf /data/web_static/current".format(env.host))
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        print("[{}] run: ln -s {} /data/web_static/current".format(env.host, archive_folder))
        run("ln -s {} /data/web_static/current".format(archive_folder))

        print("[{}] New version deployed!".format(env.host))
        return True

    except Exception as e:
        print("[{}] Deployment failed: {}".format(env.host, str(e)))
        return False
