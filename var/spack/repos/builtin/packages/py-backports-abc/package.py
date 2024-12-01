# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackportsAbc(PythonPackage):
    """Backports_ABC: A backport of recent additions to the 'collections.abc'
    module."""

    homepage = "https://github.com/cython/backports_abc"
    url = "https://github.com/cython/backports_abc/archive/0.4.tar.gz"

    license("PSF-2.0")

    version("0.5", sha256="ca1872b55cc9e19ce7288670d360104d5aac88ff1d0a0e7ad6e97267705611f9")
    version("0.4", sha256="2b5c4e91e37ba8bcd3fb8fecc8530f941578fc2c911497da3f09bf5fec6a6705")

    depends_on("py-setuptools", type="build")
