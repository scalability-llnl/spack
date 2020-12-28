# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class H5zZfp(MakefilePackage):
    """A highly flexible floating point and integer compression plugin for the
       HDF5 library using ZFP compression."""

    homepage = "http://h5z-zfp.readthedocs.io/en/latest"
    git      = "https://github.com/LLNL/H5Z-ZFP.git"

    version('develop', branch='master')
    version('0.8.0', commit='af165c4')
    version('0.7.0', commit='58ac811')

    variant('fortran', default=True, description='Enable Fortran support')

    depends_on('hdf5+fortran', when='+fortran')
    depends_on('hdf5',         when='~fortran')
    depends_on('zfp bsws=8')

    @property
    def make_defs(self):
        make_defs = [
            'PREFIX=%s' % prefix,
            'CC=%s' % spack_cc,
            'HDF5_HOME=%s' % self.spec['hdf5'].prefix,
            'ZFP_HOME=%s' % self.spec['zfp'].prefix]

        if '+fortran' in self.spec and spack_fc:
            make_defs += ['FC=%s' % spack_fc]
        else:
            make_defs += ['FC=']

        return make_defs

    @property
    def build_targets(self):
        targets = ['all']
        return self.make_defs + targets

    @property
    def install_targets(self):
        make_args = ['install']
        return make_args + self.make_defs
