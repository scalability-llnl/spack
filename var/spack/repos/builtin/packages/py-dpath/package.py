# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDpath(PythonPackage):
    """Filesystem-like pathing and searching for dictionaries."""

    homepage = "https://github.com/dpath-maintainers/dpath-python"
    pypi = "dpath/dpath-2.1.6.tar.gz"

    license("MIT")

    version("2.1.6", sha256="f1e07c72e8605c6a9e80b64bc8f42714de08a789c7de417e49c3f87a19692e47")
    version("2.0.1", sha256="bea06b5f4ff620a28dfc9848cf4d6b2bfeed34238edeb8ebe815c433b54eb1fa")

    depends_on("py-setuptools", type="build")
