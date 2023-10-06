#!/usr/bin/python3
"""a Fabric script that generates a .tgz archive from,
the contents of the web_static folder of your AirBnB Clone repo,
using the function do_pack."""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generate a .tgz archive from the contents of the web_static folder."""
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")

        now = datetime.now()
        file_name = "web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))

        local("tar -cvzf versions/{} web_static".format(file_name))

        return "versions/{}".format(file_name)
    except Exception as e:
        return None


if __name__ == "__main__":
    archive_path = do_pack()
    if archive_path:
        print("Web static packed: {}".format(archive_path))
    else:
        print("Packing failed.")
