##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import sys
import inspect
import glob
import imp

import time
import copy
import errno

from external import yaml
from external.yaml.error import MarkedYAMLError

import llnl.util.tty as tty
from llnl.util.filesystem import join_path
from llnl.util.lang import *
from llnl.util.lock import *

import spack.error
import spack.spec
from spack.spec import Spec
from spack.error import SpackError
from spack.virtual import ProviderIndex
from spack.util.naming import mod_to_class, validate_module_name


def _autospec(function):
    """Decorator that automatically converts the argument of a single-arg
       function to a Spec."""
    def converter(self, spec_like, **kwargs):
        if not isinstance(spec_like, spack.spec.Spec):
            spec_like = spack.spec.Spec(spec_like)
        return function(self, spec_like, **kwargs)
    return converter


class Database(object):
    def __init__(self,root,file_name="_index.yaml"):
        """
        Create an empty Database
        Location defaults to root/specDB.yaml
        The individual data are dicts containing
        spec: the top level spec of a package
        path: the path to the install of that package
        dep_hash: a hash of the dependence DAG for that package
        """
        self._root = root
        self._file_name = file_name
        self._file_path = join_path(self._root,self._file_name)

        self._lock_name = "_db_lock"
        self._lock_path = join_path(self._root,self._lock_name)
        if not os.path.exists(self._lock_path):
            open(self._lock_path,'w').close()
        self.lock = Lock(self._lock_path)

        self._data = []
        self._last_write_time = 0


    def _read_from_yaml(self,stream):
        """
        Fill database from YAML, do not maintain old data
        Translate the spec portions from node-dict form to spec form
        """
        try:
            file = yaml.load(stream)
        except MarkedYAMLError, e:
            raise SpackYAMLError("error parsing YAML database:", str(e))

        if file is None:
            return

        data = {}
        for index, sp in file['database'].items():
            spec = Spec.from_node_dict(sp['spec'])
            deps = sp['dependency_indices']
            path = sp['path']
            dep_hash = sp['hash']
            db_entry = {'deps':deps, 'spec': spec, 'path': path, 'hash':dep_hash}
            data[index] = db_entry

        for sph in data.values():
            for idx in sph['deps']:
                sph['spec'].dependencies[data[idx]['spec'].name] = data[idx]['spec']

        self._data = data.values()


    def read_database(self):
        """
        Re-read Database from the data in the set location
        If the cache is fresh, return immediately.
        """
        if not self.is_dirty():
            return

        if os.path.isfile(self._file_path):
            with open(self._file_path,'r') as f:
                self._read_from_yaml(f)
        else:
            #The file doesn't exist, construct from file paths
            self._data = []
            specs = spack.install_layout.all_specs()
            for spec in specs:
                sph = {}
                sph['spec']=spec
                sph['hash']=spec.dag_hash()
                sph['path']=spack.install_layout.path_for_spec(spec)
                self._data.append(sph)


    def _write_database_to_yaml(self,stream):
        """
        Replace each spec with its dict-node form
        Then stream all data to YAML
        """
        node_list = []
        spec_list = [sph['spec'] for sph in self._data]

        for sph in self._data:
            node = {}
            deps = []
            for name,spec in sph['spec'].dependencies.items():
                deps.append(spec_list.index(spec))
            node['spec']=Spec.to_node_dict(sph['spec'])
            node['hash']=sph['hash']
            node['path']=sph['path']
            node['dependency_indices']=deps
            node_list.append(node)

        node_dict = dict(enumerate(node_list))
        return yaml.dump({ 'database' : node_dict},
                         stream=stream, default_flow_style=False)


    def write(self):
        """
        Write the database to the standard location
        Everywhere that the database is written it is read
        within the same lock, so there is no need to refresh
        the database within write()
        """
        temp_name = str(os.getpid()) + socket.getfqdn() + ".temp"
        temp_file = join_path(self._root,temp_name)
        with open(temp_file,'w') as f:
            self._last_write_time = int(time.time())
            self._write_database_to_yaml(f)
        os.rename(temp_file,self._file_path)

    def is_dirty(self):
        """
        Returns true iff the database file does not exist
        or was most recently written to by another spack instance.
        """
        if not os.path.isfile(self._file_path):
            return True
        else:
            return (os.path.getmtime(self._file_path) > self._last_write_time)


#    @_autospec
    def add(self, spec, path):
        """Read the database from the set location
        Add the specified entry as a dict
        Write the database back to memory
        """
        sph = {}
        sph['spec']=spec
        sph['path']=path
        sph['hash']=spec.dag_hash()

        #Should always already be locked
        with Write_Lock_Instance(self.lock,60):
            self.read_database()
            self._data.append(sph)
            self.write()


    @_autospec
    def remove(self, spec):
        """
        Reads the database from the set location
        Searches for and removes the specified spec
        Writes the database back to memory
        """
        #Should always already be locked
        with Write_Lock_Instance(self.lock,60):
            self.read_database()

            for sp in self._data:
                #Not sure the hash comparison is necessary
                if sp['hash'] == spec.dag_hash() and sp['spec'] == spec:
                    self._data.remove(sp)

            self.write()


    @_autospec
    def get_installed(self, spec):
        """
        Get all the installed specs that satisfy the provided spec constraint
        """
        return [s for s in self.installed_package_specs() if s.satisfies(spec)]


    @_autospec
    def installed_extensions_for(self, extendee_spec):
        """
        Return the specs of all packages that extend
        the given spec
        """
        for s in self.installed_package_specs():
            try:
                if s.package.extends(extendee_spec):
                    yield s.package
            except UnknownPackageError, e:
                continue
            #skips unknown packages
            #TODO: conditional way to do this instead of catching exceptions


    def installed_package_specs(self):
        """
        Read installed package names from the database
        and return their specs
        """
        #Should always already be locked
        with Read_Lock_Instance(self.lock,60):
            self.read_database()

        installed = []
        for sph in self._data:
            installed.append(sph['spec'])
        return installed


    def installed_known_package_specs(self):
        """
        Read installed package names from the database.
        Return only the specs for which the package is known
        to this version of spack
        """
        return [s for s in self.installed_package_specs() if spack.db.exists(s.name)]

