import os
import shlex

from docker.errors import ContainerError

from app.models.configurations import Configurations
from app.ovpn.exc import RealmFullException

import app.context as ctx


def delete_first_expired():
    configurations = ctx.db.session.query(Configurations).all()
    expired = next((c for c in configurations if c.is_expired()), None)

    if not expired:
        raise RealmFullException

    ctx.db.session.query(Configurations).filter_by(username=expired.username).delete()


def revoke(username):
    try:
        ctx.dclient.containers.run(
            image="kylemanna/openvpn",
            command=shlex.split(f"ovpn_revokeclient {username} remove"),
            volumes={os.path.join(os.getcwd(), "openvpn-data"): {'bind': '/etc/openvpn', 'mode': 'ro'}},
            cap_add=["NET_ADMIN"],
            tty=True,
            remove=True
        )
    except ContainerError as e:
        print(e)
        return False

    return True
