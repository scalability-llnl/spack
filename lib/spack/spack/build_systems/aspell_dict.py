# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Why doesn't this work for me?
# from spack import *
from llnl.util.filesystem import filter_file
from spack.build_systems.autotools import AutotoolsPackage
from spack.directives import extends
from spack.package_base import ExtensionError
from spack.util.executable import which


#
# Aspell dictionaries install their bits into their prefix.lib
# and when activated they'll get symlinked into the appropriate aspell's
# dict dir (see aspell's {de,}activate methods).
#
# They aren't really an Autotools package, but it's close enough
# that this works if we override configure().
class AspellDictPackage(AutotoolsPackage):
    """Specialized class for building aspell dictionairies."""

    extends('aspell')

    def view_destination(self, view):
        aspell_spec = self.spec['aspell']
        if view.get_projection_for_spec(aspell_spec) != aspell_spec.prefix:
            raise ExtensionError(
                'aspell does not support non-global extensions')
        aspell = aspell_spec.command
        return aspell('dump', 'config', 'dict-dir', output=str).strip()

    def view_source(self):
        return self.prefix.lib

    def patch(self):
        filter_file(r'^dictdir=.*$', 'dictdir=/lib', 'configure')
        filter_file(r'^datadir=.*$', 'datadir=/lib', 'configure')

    def configure(self, spec, prefix):
        aspell = spec['aspell'].prefix.bin.aspell
        prezip = spec['aspell'].prefix.bin.prezip
        destdir = prefix

        sh = which('sh')
        sh('./configure', '--vars', "ASPELL={0}".format(aspell),
           "PREZIP={0}".format(prezip),
           "DESTDIR={0}".format(destdir))
