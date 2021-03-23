# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Ibmisc(CMakePackage):
    """Misc. reusable utilities used by IceBin."""

    homepage = "https://github.com/citibeth/ibmisc"
    url      = "https://github.com/citibeth/ibmisc/archive/v0.1.0.tar.gz"

    maintainers = ['citibeth']

    version('0.1.0', sha256='38481a8680aad4b40eca6723b2898b344cf0ef891ebc3581f5e99fbe420fa0d8')

    variant('everytrace', default=False,
            description='Report errors through Everytrace')
    variant('proj', default=True,
            description='Compile utilities for PROJ.4 library')
    variant('blitz', default=True,
            description='Compile utilities for Blitz library')
    variant('netcdf', default=True,
            description='Compile utilities for NetCDF library')
    variant('boost', default=True,
            description='Compile utilities for Boost library')
    variant('udunits2', default=True,
            description='Compile utilities for UDUNITS2 library')
    variant('googletest', default=True,
            description='Compile utilities for Google Test library')
    variant('python', default=True,
            description='Compile utilities for use with Python/Cython')

    extends('python')

    depends_on('eigen')
    depends_on('everytrace', when='+everytrace')
    depends_on('proj@:4', when='+proj')
    depends_on('blitz', when='+blitz')
    depends_on('netcdf-cxx4', when='+netcdf')
    depends_on('udunits', when='+udunits2')
    depends_on('googletest', when='+googletest', type='build')
    depends_on('py-cython', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('boost', when='+boost')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when='+boost')

    # Build dependencies
    depends_on('doxygen', type='build')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DUSE_EVERYTRACE=%s' % ('YES' if '+everytrace' in spec else 'NO'),
            '-DUSE_PROJ4=%s' % ('YES' if '+proj' in spec else 'NO'),
            '-DUSE_BLITZ=%s' % ('YES' if '+blitz' in spec else 'NO'),
            '-DUSE_NETCDF=%s' % ('YES' if '+netcdf' in spec else 'NO'),
            '-DUSE_BOOST=%s' % ('YES' if '+boost' in spec else 'NO'),
            '-DUSE_UDUNITS2=%s' % ('YES' if '+udunits2' in spec else 'NO'),
            '-DUSE_GTEST=%s' % ('YES' if '+googletest' in spec else 'NO')]
