# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------

from spack import *


class ZChecker(AutotoolsPackage):
    """a library to perform the compression assessment for lossy compressors"""

    homepage = "https://github.com/CODARcode/Z-checker"
    url      = "https://github.com/CODARcode/Z-checker/releases/download/0.7.0/Z-checker-0.7.0.tar.gz"

    maintainers = ['disheng222']

    version('0.7.0', sha256='02caf3af2dc59d116496f877da888dd2c2dffb9375c413b1d74401927963df3f')
    version('0.6.0', sha256='b01c2c78157234a734c2f4c10a7ab82c329d3cd1a8389d597e09386fa33a3117')
    version('0.5.0', sha256='ad5e68472c511b393ee1ae67d2e3072a22004001cf19a14bd99a2e322a6ce7f9')

    variant('mpi', default=False,
            description='Enable mpi compilation')

    depends_on('mpi', when="+mpi")

    def configure_args(self):
        args = []
        if '+mpi' in self.spec:
            args += ['--enable-mpi']
        else:
            args += ['--disable-mpi']
        return args

    def _test_data_property(self):
        """This test performs a test for data property analysis"""
        test_data_dir = self.test_suite.current_test_data_dir

        filename = 'testfloat_8_8_128.dat'
        orifile = test_data_dir.join(filename)

        zcconffile = 'zc.config'
        configfile = test_data_dir.join(zcconffile)

        exe='analyzeDataProperty'
        reason = 'testing data property of the command {0}'.format(exe)
        options = ['var1', '-f', configfile, orifile, '8', '8', '128']

        self.run_test(exe, options, [], installed=True, purpose=reason, skip_missing=True, work_dir=test_data_dir)

    def test(self):
        """Perform smoke tests on the installed package"""
        # test data property
        self._test_data_property()
