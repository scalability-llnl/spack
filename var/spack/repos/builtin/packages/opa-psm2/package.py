# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OpaPsm2(MakefilePackage):
    """ Intel Omni-Path Performance Scaled Messaging 2 (PSM2) library"""

    homepage = "http://github.com/intel/opa-psm2"
    url      = "https://github.com/intel/opa-psm2/archive/PSM2_10.3-8.tar.gz"

    version('11.2.77', sha256='5cc33d1e19d871a5861efe0bb897526f404b4bf2b88ac58bb277db96ac5ecb54')
    version('11.2.68', sha256='42e16a14fc8c90b50855dcea46af3315bee32fb1ae89d83060f9b2ebdce1ec26')
    version('10.3-37',  sha256='43e46f6fb345db67bb45b48e2b2bb05f590f7ccbc3ee337b33312043b46946b9')
    version('10.3-17',  sha256='17704cd4d9aeffb0d90d4ead3ad6f637bcd4cf030880e2cb2de192235859779e')
    version('10.3-10',  sha256='08d2821aa84645b93b2617dae355fcac5b690e42873c4946f2e91fa25e5a7372')
    version('10.3-8',   sha256='9ec4c2891dc3214e90f09df4d2f49b993c029279ba5d2a4306349d0ba273099e')
    version('10.2-260', sha256='825913e6a8848508eb65fa2ca97546943a90ef0c9e16dbdd543bc75b45aa51d7')
    version('10.2-235', sha256='052031ab87abadc2c11971e6aa53be363b38d58a496a6e54a820ca5bcd6545a5')
    version('10.2-175', sha256='61b694191eca66e15e7ae1659bfacb10813e569d4e27182a88fb00b5661fb365')

    variant('avx2', default=True, description='Enable AVX2 instructions')

    depends_on('numactl')

    # patch to prevent opa-psm2 from adding an additional "usr/"
    #   subdirectory within the installation prefix, which breaks paths for
    #   dependent packages like libfabric
    patch('opa-psm2-install-prefix.patch', when='@11.2.68:')

    # patch to get the Makefile to use the spack compiler wrappers
    patch('opa-psm2-compiler.patch', when='@11.2.68:',
          sha256='fe31fda9aaee13acb87d178af2282446196d2cc0b21163034573706110b2e2d6')

    def setup_build_environment(self, env):
        env.set('DESTDIR', self.prefix)
        if '%intel' in self.spec:
            # this variable must be set when we use the Intel compilers to
            # ensure that the proper flags are set
            env.set('CCARCH', 'icc')

    def edit(self, spec, prefix):
        # Change the makefile so libraries and includes are not
        # placed under $PREFIX/usr
        env['LIBDIR'] = '/lib'
        filter_file(r'${DESTDIR}/usr', '${DESTDIR}', 'Makefile')

        if '~avx2' in spec:
            env['PSM_DISABLE_AVX2'] = 'True'

    def install(self, spec, prefix):
        make('--environment-overrides', 'install')
