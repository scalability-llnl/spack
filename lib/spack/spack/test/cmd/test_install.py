##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import StringIO
import collections
import os
import unittest
import contextlib

import spack
import spack.cmd

FILE_REGISTRY = collections.defaultdict(StringIO.StringIO)


# Monkey-patch open to write module files to a StringIO instance
@contextlib.contextmanager
def mock_open(filename, mode):
    if not mode == 'wb':
        message = 'test.test_install : unexpected opening mode for mock_open'
        raise RuntimeError(message)

    FILE_REGISTRY[filename] = StringIO.StringIO()

    try:
        yield FILE_REGISTRY[filename]
    finally:
        handle = FILE_REGISTRY[filename]
        FILE_REGISTRY[filename] = handle.getvalue()
        handle.close()


# The use of __import__ is necessary to maintain a name with hyphen (which
# cannot be an identifier in python)
test_install = __import__("spack.cmd.test-install", fromlist=['test_install'])


class MockSpec(object):

    def __init__(self, name, version, hashStr=None):
        self._dependencies = {}
        self.name = name
        self.version = version
        self.hash = hashStr if hashStr else hash((name, version))

    def _deptype_norm(self, deptype):
        if deptype is None:
            return spack.alldeps
        # Force deptype to be a tuple so that we can do set intersections.
        if isinstance(deptype, str):
            return (deptype,)
        return deptype

    def _find_deps(self, where, deptype):
        deptype = self._deptype_norm(deptype)

        return [dep.spec
                for dep in where.values()
                if deptype and any(d in deptype for d in dep.deptypes)]

    def dependencies(self, deptype=None):
        return self._find_deps(self._dependencies, deptype)

    def dependents(self, deptype=None):
        return self._find_deps(self._dependents, deptype)

    def traverse(self, order=None):
        for _, spec in self._dependencies.items():
            yield spec.spec
        yield self

    def dag_hash(self):
        return self.hash

    @property
    def short_spec(self):
        return '-'.join([self.name, str(self.version), str(self.hash)])


class MockPackage(object):

    def __init__(self, spec, buildLogPath):
        self.name = spec.name
        self.spec = spec
        self.installed = False
        self.build_log_path = buildLogPath

    def do_install(self, *args, **kwargs):
        self.installed = True


class MockPackageDb(object):

    def __init__(self, init=None):
        self.specToPkg = {}
        if init:
            self.specToPkg.update(init)

    def get(self, spec):
        return self.specToPkg[spec]


def mock_fetch_log(path):
    return []

specX = MockSpec('X', "1.2.0")
specY = MockSpec('Y', "2.3.8")
specX._dependencies['Y'] = spack.DependencySpec(specY, spack.alldeps)
pkgX = MockPackage(specX, 'logX')
pkgY = MockPackage(specY, 'logY')


class MockArgs(object):

    def __init__(self, package):
        self.package = package
        self.jobs = None
        self.no_checksum = False
        self.output = None


# TODO: add test(s) where Y fails to install
class TestInstallTest(unittest.TestCase):
    """
    Tests test-install where X->Y
    """

    def setUp(self):
        super(TestInstallTest, self).setUp()

        # Monkey patch parse specs
        def monkey_parse_specs(x, concretize):
            if x == 'X':
                return [specX]
            elif x == 'Y':
                return [specY]
            return []

        self.parse_specs = spack.cmd.parse_specs
        spack.cmd.parse_specs = monkey_parse_specs

        # Monkey patch os.mkdirp
        self.os_mkdir = os.mkdir
        os.mkdir = lambda x: True

        # Monkey patch open
        test_install.open = mock_open

        # Clean FILE_REGISTRY
        FILE_REGISTRY.clear()

        pkgX.installed = False
        pkgY.installed = False

        # Monkey patch pkgDb
        self.saved_db = spack.repo
        pkgDb = MockPackageDb({specX: pkgX, specY: pkgY})
        spack.repo = pkgDb

    def tearDown(self):
        # Remove the monkey patched test_install.open
        test_install.open = open

        # Remove the monkey patched os.mkdir
        os.mkdir = self.os_mkdir
        del self.os_mkdir

        # Remove the monkey patched parse_specs
        spack.cmd.parse_specs = self.parse_specs
        del self.parse_specs
        super(TestInstallTest, self).tearDown()

        spack.repo = self.saved_db

    def test_installing_both(self):
        test_install.test_install(None, MockArgs('X'))
        self.assertEqual(len(FILE_REGISTRY), 1)
        for _, content in FILE_REGISTRY.items():
            self.assertTrue('tests="2"' in content)
            self.assertTrue('failures="0"' in content)
            self.assertTrue('errors="0"' in content)

    def test_dependency_already_installed(self):
        pkgX.installed = True
        pkgY.installed = True
        test_install.test_install(None, MockArgs('X'))
        self.assertEqual(len(FILE_REGISTRY), 1)
        for _, content in FILE_REGISTRY.items():
            self.assertTrue('tests="2"' in content)
            self.assertTrue('failures="0"' in content)
            self.assertTrue('errors="0"' in content)
            self.assertEqual(
                sum('skipped' in line for line in content.split('\n')), 2)
