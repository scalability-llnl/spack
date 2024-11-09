# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZipfileDeflate64(PythonPackage):
    """Extract Deflate64 ZIP archives with Python's zipfile API."""

    homepage = "https://github.com/brianhelba/zipfile-deflate64"
    pypi = "zipfile-deflate64/zipfile-deflate64-0.2.0.tar.gz"

    license("Apache-2.0")

    version("0.2.0", sha256="875a3299de102edf1c17f8cafcc528b1ca80b62dc4814b9cb56867ec59fbfd18")

    depends_on("c", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")
