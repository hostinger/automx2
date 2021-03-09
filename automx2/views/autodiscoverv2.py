"""
Copyright © 2019-2020 Ralph Seichter

Graciously sponsored by sys4 AG <https://sys4.de/>

This file is part of automx2.

automx2 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

automx2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with automx2. If not, see <https://www.gnu.org/licenses/>.
"""
import json

from flask import request
from flask.views import MethodView


class OutlookView(MethodView):
    """Autoconfigure mail, Outlook-style."""

    def get(self):
        request.args.get('Host')
        if request.args.get('Protocol') == "autodiscoverv1":
            value = {
                "Protocol": "AutodiscoverV1",
                "Url": "https://" + request.args.get('Host') + "/autodiscover/autodiscover.xml"
            }
            return json.dumps(value)
        return ''
