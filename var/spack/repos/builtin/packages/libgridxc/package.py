# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libgridxc(Package):
    """A library to compute the exchange and correlation energy and potential
       in spherical (i.e. an atom) or periodic systems."""

    homepage = "https://launchpad.net/libgridxc"
    url      = "https://launchpad.net/libgridxc/trunk/0.7/+download/libgridxc-0.7.6.tgz"

    version('0.7.6', sha256='ecf88ea68b9dbbdae3e86c8d598aee63b134f2f2d0e879fdedc06544b8267b91')

    phases = ['configure', 'install']

    def configure(self, spec, prefix):
        sh = which('sh')
        with working_dir('build', create=True):
            sh('../src/config.sh')
            copy('../extra/fortran.mk', 'fortran.mk')

    def install(self, spec, prefix):
        with working_dir('build'):
            make('PREFIX=%s' % self.prefix, 'FC=fc')
