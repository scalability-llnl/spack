# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
from spack.pkg.builtin.boost import Boost


class Highfive(CMakePackage):
    """HighFive - Header only C++ HDF5 interface"""

    homepage = "https://github.com/BlueBrain/HighFive"
    url      = "https://github.com/BlueBrain/HighFive/archive/v1.2.tar.gz"

    version('2.0', sha256='deee33d7f578e33dccb5d04771f4e01b89a980dd9a3ff449dd79156901ee8d25')
    version('1.5', sha256='f194bda482ab15efa7c577ecc4fb7ee519f6d4bf83470acdb3fb455c8accb407')
    version('1.2', sha256='4d8f84ee1002e8fd6269b62c21d6232aea3d56ce4171609e39eb0171589aab31')
    version('1.1', sha256='430fc312fc1961605ffadbfad82b9753a5e59482e9fbc64425fb2c184123d395')
    version('1.0', sha256='d867fe73d00817f686d286f3c69a23731c962c3e2496ca1657ea7302cd0bb944')

    variant('boost', default=False, description='Support Boost')
    variant('mpi', default=True, description='Support MPI')

    depends_on('boost @1.41:', when='+boost')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when='+boost')
    depends_on('hdf5')
    depends_on('hdf5 +mpi', when='+mpi')

    def cmake_args(self):
        args = [
            '-DUSE_BOOST:Bool={0}'.format('+boost' in self.spec),
            '-DHIGHFIVE_PARALLEL_HDF5:Bool={0}'.format('+mpi' in self.spec),
            '-DUNIT_TESTS:Bool=false',
            '-DHIGHFIVE_EXAMPLES:Bool=false']
        return args
