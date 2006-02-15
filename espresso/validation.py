# -*- coding: utf-8 -*-

# «validation» - validación de los datos de entrada del usuario
# 
# Copyright (C) 2005 Junta de Andalucía
# 
# Autor/es (Author/s):
# 
# - Antonio Olmo Titos <aolmo#emergya._info>
# - Javier Carranza <javier.carranza#interactors._coop>
# - Juan Jesús Ojeda Croissier <juanje#interactors._coop>
# 
# Este fichero es parte del instalador en directo de Guadalinex 2005.
# 
# El instalador en directo de Guadalinex 2005 es software libre. Puede
# redistribuirlo y/o modificarlo bajo los términos de la Licencia Pública
# General de GNU según es publicada por la Free Software Foundation, bien de la
# versión 2 de dicha Licencia o bien (según su elección) de cualquier versión
# posterior. 
# 
# El instalador en directo de Guadalinex 2005 se distribuye con la esperanza de
# que sea útil, pero SIN NINGUNA GARANTÍA, incluso sin la garantía MERCANTIL
# implícita o sin garantizar la CONVENIENCIA PARA UN PROPÓSITO PARTICULAR. Véase
# la Licencia Pública General de GNU para más detalles.
# 
# Debería haber recibido una copia de la Licencia Pública General junto con el
# instalador en directo de Guadalinex 2005. Si no ha sido así, escriba a la Free
# Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301
# USA.
# 
# -------------------------------------------------------------------------
# 
# This file is part of Guadalinex 2005 live installer.
# 
# Guadalinex 2005 live installer is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the License, or
# at your option) any later version.
# 
# Guadalinex 2005 live installer is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with
# Guadalinex 2005 live installer; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

""" U{pylint<http://logilab.org/projects/pylint>} mark: 6.67 """

# Validation library.
# Created by Antonio Olmo <aolmo#emergya._info> on 26 jul 2005.

from string            import whitespace, uppercase
from espresso.settings import *

def check_hostname(name):

    """ Check the correctness of a proposed host name.

        @return:
            - C{0} valid.
            - C{1} wrong length.
            - C{2} contains white spaces.
            - C{3} contains invalid characters."""

    import re
    result = [0, 0, 0]

    if len (set(name).intersection(set(whitespace))) > 0:
        result[1] = 2
    if len (name) < 3 or len (name) > 18:
        result[0] = 1

    regex = re.compile(r'^[a-zA-Z0-9]+$')
    if not regex.search(name):
      result[2] = 3

    return result

def check_mountpoint(mountpoints, size):

    """ Check the correctness of a proposed set of mountpoints.

        @return:
            - C{0} Doesn't exist root path.
            - C{1} Path duplicated.
            - C{2} Size incorrect.
            - C{3} Contains invalid characters."""

    import re
    result = [0, 0, 0, 0]
    root = 0

    if 'swap' in mountpoints.values():
      root_minimum_KB = MINIMAL_PARTITION_SCHEME['root'] * 1024
    else:
      root_minimum_KB = (MINIMAL_PARTITION_SCHEME['root'] +
                         MINIMAL_PARTITION_SCHEME['swap']) * 1024

    for device, path in mountpoints.items():
      if path == '/':
        root = 1

        if float(size[device.split('/')[2]]) < root_minimum_KB:
          result[2] = 3

      if mountpoints.values().count(path) > 1:
        result[1] = 2
      regex = re.compile(r'^[a-zA-Z0-9/\-\_\+]+$')
      if not regex.search(path):
        result[3] = 4

    if root != 1:
      result[0] = 1

    return result
