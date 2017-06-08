from __future__ import print_function, absolute_import, division
from future.builtins import *
from future import standard_library
standard_library.install_aliases()

# Copyright 2017 Autodesk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This module provides access to the chemical component database, which is stored in
``moldesign/_static_data/chemical_components``

and can be re-generated by running

``cd moldesign/_static_data/ && scripts/generate_residue_data.py --download``
"""
import os

from . import PACKAGEPATH
from moldesign import utils


class _DatabaseEntry(object):
    """ Maps into a field stored in the database
    """
    def __init__(self, hostdb, keyname):
        self.hostdb = hostdb
        self.keyname = keyname
        self.index = self.hostdb['__FIELDS__']['RESFIELDS'].index(keyname)

    def __repr__(self):
        return '<Chemical component dictionary: "%s" entries>' % self.keyname

    def __getitem__(self, item):
        return self.hostdb[item][self.index]

    __contains__ = utils.Alias('hostdb.__contains__')

    def keys(self):
        for key in self.hostdb.keys():
            if key == '__FIELDS__':
                continue
            yield key

    def items(self):
        for key in self:
            yield key, self[key]

    __iter__ = keys


# This is a very big dict, so we load it as a compressed database
_bondfilename = os.path.join(PACKAGEPATH, '_static_data', 'chemical_components')
CCD_DATABASE = utils.CompressedJsonDbm(_bondfilename, 'r', dbm=utils.ReadOnlyDumb)
RESIDUE_BONDS = _DatabaseEntry(CCD_DATABASE, 'bonds')
RESIDUE_ATOMS = _DatabaseEntry(CCD_DATABASE, 'atoms')
RESIDUE_CCD_NAMES = _DatabaseEntry(CCD_DATABASE, 'name')
RESIDUE_CCD_TYPES = _DatabaseEntry(CCD_DATABASE, 'type')
