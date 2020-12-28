# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack.package import *


class PyFparser(PythonPackage):
    """Parser for Fortran 77..2003 code."""

    homepage = "https://github.com/stfc/fparser"
    url      = "https://github.com/stfc/fparser/archive/0.0.5.tar.gz"
    git      = "https://github.com/stfc/fparser.git"

    version('develop', branch='master')
    version('0.0.6', sha256='6ced61573257d11037d25c02d5f0ea92ca9bf1783018bf5f0de30d245ae631ac')
    version('0.0.5', sha256='7668b331b9423d15353d502ab26d1d561acd5247882dab672f1e45565dabaf08')

    depends_on('py-setuptools', type='build')

    depends_on('py-numpy', type=('build', 'run'), when='@:0.0.5')
    depends_on('py-nose', type='build')
    depends_on('py-six', type='build', when='@0.0.6:')

    depends_on('py-pytest', type='test')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_build(self):
        # Ensure that pytest.ini exists inside the source tree,
        # otherwise an external pytest.ini can cause havoc:
        touch('pytest.ini')
        with working_dir('src'):
            Executable('py.test')()
