# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonMeep(PythonPackage):
    """Python-meep is a wrapper around libmeep. It allows the scripting of
    Meep-simulations with Python"""

    homepage = "https://launchpad.net/python-meep"
    url      = "https://launchpad.net/python-meep/1.4/1.4/+download/python-meep-1.4.2.tar"

    version('1.4.2', sha256='d91428aa4727c308383cea31ca9cdacee409320c686e9a8368769933e56c8762')

    variant('mpi', default=True, description='Enable MPI support')

    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))

    depends_on('mpi', when='+mpi')
    depends_on('meep~mpi', when='~mpi')
    depends_on('meep+mpi', when='+mpi')

    # As of SWIG 3.0.3, Python-style comments are now treated as
    # pre-processor directives. Use older SWIG. But not too old,
    # or else it can't handle newer C++ compilers and flags.
    depends_on('swig@1.3.39:3.0.2')

    phases = ['clean', 'build_ext', 'install', 'bdist']

    def setup_file(self):
        return 'setup-mpi.py' if '+mpi' in self.spec else 'setup.py'

    def common_args(self, spec, prefix):
        include_dirs = [
            spec['meep'].prefix.include,
            os.path.join(
                spec['py-numpy'].prefix,
                spec['python'].package.python_include_dir
            )
        ]

        library_dirs = [
            spec['meep'].prefix.lib
        ]

        if '+mpi' in spec:
            include_dirs.append(spec['mpi'].prefix.include)
            library_dirs.append(spec['mpi'].prefix.lib)

        include_flags = '-I{0}'.format(','.join(include_dirs))
        library_flags = '-L{0}'.format(','.join(library_dirs))

        # FIXME: For some reason, this stopped working.
        # The -I and -L are no longer being properly forwarded to setup.py:
        # meep_common.i:87: Error: Unable to find 'meep/mympi.hpp'
        # meep_common.i:88: Error: Unable to find 'meep/vec.hpp'
        # meep_common.i:89: Error: Unable to find 'meep.hpp'

        return [include_flags, library_flags]

    def clean_args(self, spec, prefix):
        return ['--all']

    def build_ext_args(self, spec, prefix):
        return self.common_args(spec, prefix)

    def bdist_args(self, spec, prefix):
        return self.common_args(spec, prefix)
