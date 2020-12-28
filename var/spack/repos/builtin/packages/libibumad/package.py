# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libibumad(CMakePackage):
    """This package installs the user-space libraries and headers for libibumad.
       This is a subset of the linux-rdma distribution."""

    homepage = "https://github.com/linux-rdma/"
    url      = "https://github.com/linux-rdma/rdma-core/archive/v25.0.tar.gz"

    version('25.0', sha256='d735bd091d13e8a68ce650e432b5bdc934fc7f1d5fb42a6045278a5b3f7fe48b')

    depends_on('libnl')

    def build(self, spec, prefix):
        with working_dir(join_path(self.build_directory, 'libibumad')):
            make()

    def install(self, spec, prefix):
        with working_dir(join_path(self.build_directory, 'libibumad')):
            make('install')
