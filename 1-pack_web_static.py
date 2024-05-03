#!/usr/bin/python3
"""
Python script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo.
"""
import os
import tarfile
from datetime import datetime


def do_pack():
    """
    Compresses the web_static folder into a .tgz archive

    Returns:
        str: Path to the newly created archive, or None if the operation fails
    """
    try:
        current_time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_path = "versions/web_static_{}.tgz".format(current_time)

        # Create versions directory if it doesn't exist
        if not os.path.exists("versions"):
            os.makedirs("versions")

        # Create a tarball of the web_static folder
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add("web_static", arcname=os.path.basename("web_static"))
        archive_size = os.path.getsize(archive_path)
        print("web_static packed: {} -> {}Bytes".format(
            archive_path, archive_size
        ))

        return archive_path
    except Exception as e:
        print("Error:", e)
        return None


if __name__ == "__main__":
    do_pack()
