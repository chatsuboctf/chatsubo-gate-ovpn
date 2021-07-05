import os
import shlex
from uuid import uuid4

from docker.errors import ContainerError, ImageNotFound, APIError
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app.models.configurations import Configurations
import app.context as ctx


class OpenVPNManager:

    def get(self, username):
        conf = ctx.db.session.query(Configurations).filter_by(username=username).first()
        if not conf:
            return None

        return conf.config

    def create(self, username):
        try:
            ctx.dclient.images.get("kylemanna/openvpn")
        except ImageNotFound:
            try:
                ctx.dclient.images.pull("kylemanna/openvpn")
            except APIError as e:
                print(e)
                return None

        try:
            ctx.dclient.containers.run(
                image="kylemanna/openvpn",
                command=shlex.split(f"easyrsa build-client-full {username} nopass"),
                volumes={"/etc/openvpn": {'bind': '/etc/openvpn', 'mode': 'rw'}},
                cap_add=["NET_ADMIN"],
                environment=[f"EASYRSA_PASSIN=pass:{current_app.config['ca_pass']}"],
                remove=True
            )
        except ContainerError as e:
            print(e)
            return None

        try:
            conf_content = ctx.dclient.containers.run(
                image="kylemanna/openvpn",
                command=shlex.split(f"ovpn_getclient {username}"),
                volumes={"/etc/openvpn": {'bind': '/etc/openvpn', 'mode': 'ro'}},
                cap_add=["NET_ADMIN"],
                tty=True,
                remove=True
            )
        except ContainerError as e:
            print(e)
            return None

        try:
            conf = Configurations(id=str(uuid4()), username=username, config=conf_content.decode())
            ctx.db.session.add(conf)
            ctx.db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            return None

        return conf_content.decode()

        # Run docker to create username's config
        # Store it in db and returns it

        # if conf in db, return imediately
        # if not, create it, create conf and return content

    # def add_peer(self, username):
    #     config = Configurations(username=username)
    #
    #     return config
