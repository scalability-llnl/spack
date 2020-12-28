# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastrlock(PythonPackage):
    """This is a C-level implementation of a fast, re-entrant,
    optimistic lock for CPython."""

    homepage = "https://github.com/scoder/fastrlock"
    url      = "https://github.com/scoder/fastrlock/archive/0.5.tar.gz"

    version('0.5', sha256='756dd8aa9af9848caa9bbf814c4dec1065ee38cc38768158e616ec11b6f45cc8')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')

    def build_args(self, spec, prefix):
        args = []
        args.append('--with-cython')
        return args
