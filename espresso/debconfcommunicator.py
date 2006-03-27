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

import popen2
import debconf

class DebconfCommunicator(debconf.Debconf, object):
    def __init__(self, owner, title=None):
        self.dccomm = popen2.Popen3(['debconf-communicate', '-fnoninteractive',
                                     owner])
        super(DebconfCommunicator, self).__init__(title=title,
                                                  read=self.dccomm.fromchild,
                                                  write=self.dccomm.tochild)

    def shutdown(self):
        if self.dccomm is not None:
            self.dccomm.tochild.close()
            self.dccomm.fromchild.close()
            self.dccomm.wait()
            self.dccomm = None

    def __del__(self):
        self.shutdown()
