# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class FrontierClient(MakefilePackage):
    """The Frontier distributed database caching system distributes data from
       data sources to many client systems around the world. The name comes
       from "N Tier" where N is any number and tiers are layers of locations
       of distribution."""

    homepage = "http://frontier.cern.ch/"
    url      = "https://github.com/fermitools/frontier/archive/v2_9_1.tar.gz"

    version('2_9_1',  sha256='d21370fbe142807966e3c2218ce361ea3bb573498e1b8387b801fb6641c3ed22')
    version('2_9_0',  sha256='e58dba3f177c5b74609f244101a22a5c14d42bf019013fe2dba72c09f819c62a')
    version('2_8_21', sha256='7df9ba61c3e1778aca75c5da6e45ee4d00b5c061d3f7162208e2fbd2ec266a9e')
    version('2_8_20', sha256='81b0f45762d96a33f156e0238631a60eef910a176644e95c6c19a36824bef7e1')

    depends_on('pacparser')
    depends_on('expat')

    patch('frontier-client.patch', level=0)

    def edit(self, spec, prefix):
        makefile = FileFilter('client/Makefile')
        makefile.filter('EXPAT_DIR}/lib', 'EXPAT_DIR}/lib64')

    def build(self, spec, prefix):
        with working_dir('client'):
            make('-j1', 'dist', 'PACPARSER_DIR=' + self.spec['pacparser'].prefix,
                 'EXPAT_DIR=' + self.spec['expat'].prefix)

    def install(self, spec, prefix):
        install_tree(join_path('client', 'dist'), prefix)
