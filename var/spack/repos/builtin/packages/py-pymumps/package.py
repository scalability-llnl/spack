# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPymumps(PythonPackage):
    """Python bindings for MUMPS, a parallel sparse direct solver"""

    homepage = "http://github.com/pymumps/pymumps"
    pypi = "PyMUMPS/PyMUMPS-0.3.2.tar.gz"
    git = "https://github.com/PyMumps/pymumps.git"

    # Add a list of GitHub accounts to notify when the
    # package is updated
    maintainers = ['payerle']

    version('0.3.2', sha256='f290ec4850098f108fb91cb9e7fa07302ebf5076e4329f8e6ea4924de8ba35df')

    depends_on('py-cython', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('mumps', type='link')
    depends_on('py-mpi4py', type=('build', 'run'))

    # Patch to add libmumps_common.so to library dependencies
    # See https://github.com/PyMumps/pymumps/issues/13
    patch('py-pymumps.setup.patch')

    phases = ['build_ext', 'install']

    def build_ext_args(self, spec, prefix):
        # Requires --library-dirs,
        # '--libraries', spec['mumps'].prefix.libs, does not cut it
        args = ['--include-dirs',
                spec['mumps'].prefix.include,
                '--library-dirs',
                spec['mumps'].libs.directories[0],
                '--rpath',
                spec['mumps'].libs.directories[0],
                '-l', 'dmumps',
                '-l', 'mumps_common',
                '-l', 'pord',
                ]
        return args
