# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libseccomp(AutotoolsPackage):
    """The main libseccomp repository"""

    homepage = "https://github.com/seccomp/libseccomp"
    url      = "https://github.com/seccomp/libseccomp/archive/v2.3.3.zip"

    version('2.3.3', sha256='627e114b3be2e66ed8d88b90037498333384d9bea822423662a44c3a8520e187')

    variant('python', default=True, description="Build Python bindings")

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on("py-cython", type="build", when="+python")

    def configure_args(self):
        args = []
        if "+python" in self.spec:
            args.append("--enable-python")
        return args
