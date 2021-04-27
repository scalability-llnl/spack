# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyVermin(PythonPackage):
    """Concurrently detect the minimum Python versions needed to run code."""

    homepage = "https://github.com/netromdk/vermin"
    url      = "https://github.com/netromdk/vermin/archive/v1.1.1.tar.gz"

    maintainers = ['netromdk']

    version('1.1.1', sha256='d13b2281ba16c9d5b0913646483771789552230a9ed625e2cd92c5a112e4ae80')
    version('1.1.0', sha256='62d9f1b6694f50c22343cead2ddb6e2b007d24243fb583f61ceed7540fbe660b')
    version('1.0.3', sha256='1503be05b55cacde1278a1fe55304d8ee889ddef8ba16e120ac6686259bec95c')
    version('1.0.2', sha256='e999d5f5455e1116b366cd1dcc6fecd254c7ae3606549a61bc044216f9bb5b55')
    version('1.0.1', sha256='c06183ba653b9d5f6687a6686da8565fb127fab035f9127a5acb172b7c445079')
    version('1.0.0', sha256='e598e9afcbe3fa6f3f3aa894da81ccb3954ec9c0783865ecead891ac6aa57207')
    version('0.10.5', sha256='00601356e8e10688c52248ce0acc55d5b45417b462d5aa6887a6b073f0d33e0b')
    version('0.10.4', sha256='bd765b84679fb3756b26f462d2aab4af3183fb65862520afc1517f6b39dea8bf')
    version('0.10.0', sha256='3458a4d084bba5c95fd7208888aaf0e324a07ee092786ee4e5529f539ab4951f')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def build_test(self):
        make('test')
