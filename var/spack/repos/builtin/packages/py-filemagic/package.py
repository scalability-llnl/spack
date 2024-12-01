# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFilemagic(PythonPackage):
    """A Python API for libmagic, the library behind the Unix file command"""

    homepage = "https://filemagic.readthedocs.io/en/latest/"
    pypi = "filemagic/filemagic-1.6.tar.gz"

    license("Apache-2.0")

    version("1.6", sha256="e684359ef40820fe406f0ebc5bf8a78f89717bdb7fed688af68082d991d6dbf3")

    depends_on("py-setuptools", type="build")
    depends_on("file", type="run")
