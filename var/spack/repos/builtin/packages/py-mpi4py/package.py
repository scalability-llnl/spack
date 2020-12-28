# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMpi4py(PythonPackage):
    """This package provides Python bindings for the Message Passing
       Interface (MPI) standard. It is implemented on top of the
       MPI-1/MPI-2 specification and exposes an API which grounds on the
       standard MPI-2 C++ bindings.
    """
    homepage = "https://pypi.python.org/pypi/mpi4py"
    url      = "https://pypi.io/packages/source/m/mpi4py/mpi4py-3.0.3.tar.gz"
    git      = "https://github.com/mpi4py/mpi4py.git"

    version('develop', branch='master')
    version('3.0.3', sha256='012d716c8b9ed1e513fcc4b18e5af16a8791f51e6d1716baccf988ad355c5a1f')
    version('3.0.1', sha256='6549a5b81931303baf6600fa2e3bc04d8bd1d5c82f3c21379d0d64a9abcca851')
    version('3.0.0', sha256='b457b02d85bdd9a4775a097fac5234a20397b43e073f14d9e29b6cd78c68efd7')
    version('2.0.0', sha256='6543a05851a7aa1e6d165e673d422ba24e45c41e4221f0993fe1e5924a00cb81')
    version('1.3.1', sha256='e7bd2044aaac5a6ea87a87b2ecc73b310bb6efe5026031e33067ea3c2efc3507')

    depends_on('python@2.6:2.7.99,3.2:')
    depends_on('py-setuptools', type='build')
    depends_on('mpi')
    depends_on('py-cython@0.22.0:', when='@develop', type='build')

    def build_args(self, spec, prefix):
        return ['--mpicc=%s -shared' % spec['mpi'].mpicc]

    @property
    def headers(self):
        headers = find_all_headers(self.prefix.lib)
        return headers
