# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack.package import *


class PyPsyclone(PythonPackage):
    """Code generation for the PSyKAl framework from the GungHo project,
       as used by the LFRic model at the UK Met Office."""

    homepage = "https://github.com/stfc/PSyclone"
    url      = "https://github.com/stfc/PSyclone/archive/1.5.1.tar.gz"
    git      = "https://github.com/stfc/PSyclone.git"

    version('develop', branch='master')
    version('1.5.1', commit='eba7a097175b02f75dec70616cf267b7b3170d78')

    depends_on('py-setuptools', type='build')
    depends_on('py-pyparsing', type=('build', 'run'))

    # Test cases fail without compatible versions of py-fparser:
    depends_on('py-fparser@0.0.5', type=('build', 'run'), when='@1.5.1')
    depends_on('py-fparser', type=('build', 'run'), when='@1.5.2:')

    # Dependencies only required for tests:
    depends_on('py-numpy',  type='test')
    depends_on('py-nose',   type='test')
    depends_on('py-pytest', type='test')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_build(self):
        # Limit py.test to search inside the build tree:
        touch('pytest.ini')
        with working_dir('src'):
            Executable('py.test')()

    def setup_build_environment(self, env):
        # Allow testing with installed executables:
        env.prepend_path('PATH', self.prefix.bin)
