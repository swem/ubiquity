# -*- coding: UTF-8 -*-

# Copyright (C) 2005 Canonical Ltd.
# Written by Colin Watson <cjwatson@ubuntu.com>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from oem_config.filteredcommand import FilteredCommand

# TODO: skip this if there's already a user configured, or re-ask and create
# a new one, or what?
class User(FilteredCommand):
    def prepare(self):
        questions = ['^passwd/user-fullname$', '^passwd/username$',
                     '^passwd/user-password$', '^passwd/user-password-again$',
                     'ERROR']
        return (['/usr/lib/oem-config/user/user-setup', '/'], questions)

    def set(self, question, value):
        if question == 'passwd/username':
            if self.frontend.get_username() != '':
                self.frontend.set_username(value)

    def ok_handler(self):
        fullname = self.frontend.get_fullname()
        username = self.frontend.get_username()
        password = self.frontend.get_password()
        password_confirm = self.frontend.get_verified_password()

        self.preseed('passwd/user-fullname', fullname)
        self.preseed('passwd/username', username)
        # TODO: maybe encrypt these first
        self.preseed('passwd/user-password', password, escape=True)
        self.preseed('passwd/user-password-again', password_confirm,
                     escape=True)
        self.preseed('passwd/user-uid', '')

        super(User, self).ok_handler()

    def error(self, priority, question):
        self.frontend.error_dialog(self.description(question),
                                   self.extended_description(question))
        return super(User, self).error(priority, question)
