# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFortranformat(PythonPackage):
    """Mimics Fortran textual IO in Python"""

    homepage = "https://github.com/brendanarnold/py-fortranformat"
    pypi = "fortranformat/fortranformat-2.0.0.tar.gz"

    license("MIT")

    version("2.0.0", sha256="52473831d6f6bad7c2de0f26ad51856ea5d0ef097bcba5af3b855b871b815b0d")
    version("1.2.2", sha256="a8c41ab39bb40444e6ca17f38755d64df51799b064206833c137a28bbdca1b2b")
    version("1.1.1", sha256="9b7aa2148af7a5f4f5fd955d121bd6869d44b82ac2182d459813b849aa87d831")
    version("0.2.5", sha256="6b5fbc1f129c7a70543c3a81f334fb4d57f07df2834b22ce69f6d7e8539cd3f9")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
