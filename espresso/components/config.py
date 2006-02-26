# -*- coding: UTF-8 -*-

# Copyright (C) 2006 Canonical Ltd.
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

from espresso.filteredcommand import FilteredCommand

class Config(FilteredCommand):
    def prepare(self):
        questions = ['^grub-installer/apt-install-failed$',
                     'ERROR',
                     'PROGRESS']
        return (['/usr/share/espresso/config.py'], questions)

    def error(self, priority, question):
        self.frontend.error_dialog(self.description(question))
        return super(Config, self).error(priority, question)
