# !/usr/bin/env python3
# Copyright (C) 2017  Qrama
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# pylint: disable=c0111,c0301,c0325, r0903,w0406
from charms.reactive import Endpoint, when_any, set_flag, clear_flag, when_not


class ArangoDBRequires(Endpoint):

    @when_any('endpoint.{endpoint_name}.joined')
    def joined(self):
        if any(unit.received.get('port') for unit in self.all_joined_units):
            set_flag(self.expand_name('endpoint.{endpoint_name}.available'))
        else:
            clear_flag(self.expand_name('endpoint.{endpoint_name}.available'))

    @when_any('endpoint.{endpoint_name}.changed',
              'endpoint.{endpoint_name}.departed')
    def changed(self):
        set_flag(self.expand_name('endpoint.{endpoint_name}.update'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.departed'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.changed'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('endpoint.{endpoint_name}.available'))

    def relation_data(self):
        data = []
        for unit in self.all_joined_units:
            port = unit.received.get('port')
            host = unit.received.get('host')
            username = unit.received.get('username')
            password = unit.received.get('password')
            if port and host and username:
                data.append({
                    'host': host,
                    'port': port,
                    'username': username,
                    'password': password,
                    'remote_unit_name': unit.unit_name
                })
        return data
