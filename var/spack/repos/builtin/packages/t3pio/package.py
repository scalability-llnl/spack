# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install t3pio
#
# You can edit this file again by typing:
#
#     spack edit t3pio
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class T3pio(AutotoolsPackage):
    """TACC's Terrific Tool for Parallel I/O"""

    homepage = "https://github.com/TACC/t3pio"
    url      = "https://github.com/TACC/t3pio/archive/2.4.tar.gz"
    git      = "https://github.com/TACC/t3pio.git"

    # maintainers = ['rtmclay', 'ax3l']

    version('2.4', sha256='c4f61a893e54dbea4f680e9417c5effa15a3cfb125546bf2747851cce3c1c844')

    variant('shared', default=True,
            description='Builds a shared version of the library')
    #variant('fortran', default=False,
    #        description='Enable Fortran bindings support')
    variant('hdf5', default=False,
            description='Build with parallel HDF5')

    parallel = False
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('m4', type='build')
    depends_on('libtool', type='build')

    depends_on('mpi')
    depends_on('hdf5 +mpi', when='+hdf5')

    def setup_build_environment(self, env):
        env.set('FC', self.spec['mpi'].mpifc)
        env.set('F77', self.spec['mpi'].mpif77)
        #if self.spec.satisfies('%gcc@10: +fortran'):
        #    env.set('FCFLAGS', '-fallow-argument-mismatch')

    def configure_args(self):
        spec = self.spec
        args = []

        # required, otherwise "use mpi" is not found
        #extra_args = ['FC=%s' % spec['mpi'].mpifc]

        args += self.enable_or_disable('shared')
        # configure: WARNING: unrecognized options: --disable-fortran, --with-mpi
        #args += self.enable_or_disable('fortran')
        #args += ['--with-mpi={0}'.format(spec['mpi'].prefix)]

        if spec.satisfies('+hdf5'): 
            args += ['--with-phdf5={0}'.format(
                spec['hdf5'].prefix
            )]
        else:
            args += ['--without-phdf5']

        # Future:
        #  --with-lustreMaxStripesPerFile=ans
        #                  Max stripes possible with lustre, Lustre 2.1 ==>
        #                  160, Lustre 2.4 ==> 2000 [[160]]
        #  --with-goodCitzenshipStripes=ans
        #                  Max number of stripes in automatic mode [[80]]
        #  --with-maxStripesPerNode=ans
        #                  Max number of stripes for a single node [[4]]
        #  --with-lustre   lustre filesystem string: /scratch:90:/work:30:

        return args
