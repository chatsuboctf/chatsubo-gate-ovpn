from flask_restx import Resource

from app.api import vpn_api
from app.helpers.api_response import VpnAccessApiResponse

import app.context as ctx
from app.helpers.auth import require_auth
from app.helpers.configurations import delete_first_expired, revoke
from app.models.configurations import Configurations
from app.ovpn.exc import RealmFullException
from app.ovpn.manager import OpenVPNManager


@vpn_api.route('/get/<string:username>')
class List(Resource):

    @require_auth
    def get(self, username):
        res = VpnAccessApiResponse()
        ovpn = OpenVPNManager()

        conf = ovpn.get(username)
        if conf:
            res.config = conf
            return res.make()

        peers_qty = ctx.db.session.query(Configurations).count()
        if peers_qty == 254:
            try:
                delete_first_expired()
            except RealmFullException:
                res.add_error("Realm is full")
                return res.make()

            revoke(username)

        res.config = ovpn.create(username)

        return res.make()
