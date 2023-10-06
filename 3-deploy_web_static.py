#!/usr/bin/python3
"""a Fabric script (based on the file 2-do_deploy_web_static.py),
that creates and distributes an archive to your web servers,
using the function deploy"""

from fabric.api import env, run, put, local
from os.path import exists
from datetime import datetime
from os import makedirs

env.user = 'ubuntu'
env.hosts = ['<IP_web-01>', '<IP_web-02>']  # Replace with actual IP addresses


def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder.
    """
    try:
        # Create the 'versions' directory if it doesn't exist
        if not exists("versions"):
            makedirs("versions")

        now = datetime.now()
        file_name = "web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))

        # Execute the tar command to create the .tgz archive
        local("tar -cvzf versions/{} web_static".format(file_name))

        # Return the path of the archive
        return "versions/{}".format(file_name)
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Distribute an archive to the web servers and deploy it.

    Args:
        archive_path (str): Path to the archive to be deployed.

    Returns:
        bool: True if successful, False otherwise.
    """
    if not exists(archive_path):
        print("Archive not found.")
        return False

    try:
        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Extract the archive to the appropriate directory
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]
        release_path = "/data/web_static/releases/{}/".format(folder_name)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, release_path))

        # Delete the uploaded archive
        run("rm /tmp/{}".format(file_name))

        # Move the contents of the release to the correct location
        run("mv {}web_static/* {}".format(release_path, release_path))
        run("rm -rf {}web_static".format(release_path))

        # Update the symbolic link
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed: {}".format(str(e)))
        return False


def deploy():
    # Call do_pack and store the archive path
    archive_path = do_pack()

    # Return False if no archive has been created
    if not archive_path:
        return False

    # Call do_deploy with the new path of the archive
    return do_deploy(archive_path)


if __name__ == "__main__":
    # Execute the deploy function
    deploy()
