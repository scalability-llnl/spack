# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nco(AutotoolsPackage):
    """The NCO toolkit manipulates and analyzes data stored in
    netCDF-accessible formats"""

    homepage = "http://nco.sourceforge.net/"
    url      = "https://github.com/nco/nco/archive/4.6.7.tar.gz"

    version('4.9.3', sha256='eade5b79f3814b11ae3f52c34159567e76a73f05f0ab141eccaac68f0ca94aee')
    version('4.9.2', sha256='1a98c37c946c00232fa7319d00d1d80f77603adda7c9239d10d68a8a3545a4d5')
    version('4.9.1', sha256='9592efaf0dfd6ccdefd0b417d990cfccae7e89c20d90fb44ead6263009778834')
    version('4.9.0', sha256='21dd53f427793cbc52d1c007e9b7339c83f6944a937a1acfbbe733e49b65378b')
    version('4.8.1', sha256='ddae3fed46c266798ed1176d6a70b36376d2d320fa933c716a623172d1e13c68')
    version('4.8.0', sha256='91f95ebfc9baa888adaec3016ca18a6297e2881b1429d74543a27fdfbe15fcab')
    version('4.7.9', sha256='048f6298bceb40913c3ae433f875dea1e9129b1c86019128e7271d08f274a879')
    version('4.6.7', sha256='2fe2dabf14a60bface694307cbe719df57103682b715348e9d77bfe8d31487f3')
    version('4.6.6', sha256='079d83f800b73d9b12b8de1634a88c2cbe40a639aaf7bc056cd2e836c6047697')
    version('4.6.5', sha256='d5b18c9ada25d062a539e2995be445db39e8021c56cd4b20c88485cb2452c7ae')
    version('4.6.4', sha256='1c2ab906fc81f91bf8aff3e6da27ae7a4c89821c5836d787188fff5262418062')
    version('4.6.3', sha256='414ccb349ed25cb37b669fb87f9e2e4ca8d58c2f45538feda199bf895b982bf8')
    version('4.6.2', sha256='cec82e35d47a6bbf8ab9301d5ff4cf08051f489b49e8529ebf780380f2c21ed3')
    version('4.6.1', sha256='7433fe5901f48eb5170f24c6d53b484161e1c63884d9350600070573baf8b8b0')
    version('4.5.5', sha256='bc6f5b976fdfbdec51f2ebefa158fa54672442c2fd5f042ba884f9f32c2ad666')

    # https://github.com/nco/nco/issues/43
    patch('NUL-0-NULL.patch', when='@:4.6.7')

    variant('doc', default=False, description='Build/install NCO TexInfo-based documentation')

    # See "Compilation Requirements" at:
    # http://nco.sourceforge.net/#bld
    depends_on('netcdf-c')
    depends_on('antlr@2.7.7+cxx')  # required for ncap2
    depends_on('gsl')              # desirable for ncap2
    depends_on('udunits')          # allows dimensional unit transformations

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('texinfo@4.12:', type='build', when='+doc')

    conflicts('%gcc@9:', when='@:4.7.8')

    def configure_args(self):
        spec = self.spec
        return ['--{0}-doc'.format('enable' if '+doc' in spec else 'disable')]

    def setup_build_environment(self, env):
        spec = self.spec
        env.set('NETCDF_INC', spec['netcdf-c'].prefix.include)
        env.set('NETCDF_LIB', spec['netcdf-c'].prefix.lib)
        env.set('ANTLR_ROOT', spec['antlr'].prefix)
        env.set('UDUNITS2_PATH', spec['udunits'].prefix)
