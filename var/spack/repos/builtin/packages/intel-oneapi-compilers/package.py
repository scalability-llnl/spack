# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import subprocess

from spack import *


releases = {'2021.1.0':
            {'irc_id': '17427', 'build': '2684'}}


class IntelOneapiCompilers(IntelOneApiPackage):
    """Intel oneAPI compilers.

    Contains icc, icpc, icx, icpx, dpcpp, ifort, ifx.

    """

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/dpc-compiler.html'

    version('2021.1.0', sha256='666b1002de3eab4b6f3770c42bcf708743ac74efeba4c05b0834095ef27a11b9', expand=False)

    depends_on('patchelf', type='build')

    def __init__(self, spec):
        self.component_info(
            dir_name='compiler',
            components=('intel.oneapi.lin.dpcpp-cpp-compiler-pro'
                        ':intel.oneapi.lin.ifort-compiler'),
            releases=releases,
            url_name='HPCKit')
        super(IntelOneapiCompilers, self).__init__(spec)

    def _join_prefix(self, path):
        return join_path(self.prefix, 'compiler', 'latest', 'linux', path)

    def _ld_library_path(self):
        dirs = ['lib',
                'lib/x64',
                'lib/emu',
                'lib/oclfpga/host/linux64/lib',
                'lib/oclfpga/linux64/lib',
                'compiler/lib/intel64_lin',
                'compiler/lib']
        for dir in dirs:
            yield self._join_prefix(dir)

    def install(self, spec, prefix):
        # For quick turnaround debugging, comment out line below and
        # use the copy instead
        super(IntelOneapiCompilers, self).install(spec, prefix)
        # Copy installed compiler instead of running the installer
        # from shutil import copytree
        # copytree('/opt/intel/oneapi/compiler', join_path(prefix, 'compiler'),
        #         symlinks=True)

        rpath = ':'.join(self._ld_library_path())
        patch_dirs = ['compiler/lib/intel64_lin',
                      'compiler/lib/intel64',
                      'bin']
        for pd in patch_dirs:
            for file in glob.glob(self._join_prefix(join_path(pd, '*'))):
                # Try to patch all files, patchelf will do nothing if
                # file should not be patched
                subprocess.call(['patchelf', '--set-rpath', rpath, file])

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self._join_prefix('bin'))
        env.prepend_path('PATH', self._join_prefix('bin/intel64'))
        env.prepend_path('MANPATH', self._join_prefix('../documentation/en/man/common'))
        env.prepend_path('CPATH', self._join_prefix('include'))
        env.prepend_path('LIBRARY_PATH', self._join_prefix('lib'))
        env.prepend_path('LIBRARY_PATH', self._join_prefix('lib/intel64_lin'))
        env.prepend_path('OCL_ICD_FILENAMES',
                         self._join_prefix('lib/x64/libintelocl.so'))
        for dir in self._ld_library_path():
            env.prepend_path('LD_LIBRARY_PATH', dir)
        env.set('CC', self._join_prefix('bin/icx'))
        env.set('CXX', self._join_prefix('bin/icpx'))
        env.set('FC', self._join_prefix('bin/ifx'))
        # Set these so that MPI wrappers will pick up these compilers
        # when this module is loaded.
        env.set('I_MPI_CC', 'icx')
        env.set('I_MPI_CXX', 'icpx')
        env.set('I_MPI_FC', 'ifx')
