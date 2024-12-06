# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJarowinkler(PythonPackage):
    """library for fast approximate string matching using Jaro and Jaro-Winkler similarity."""

    homepage = "https://github.com/maxbachmann/JaroWinkler"
    pypi = "jarowinkler/jarowinkler-1.2.3.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version("1.2.3", sha256="af28ea284cfbd1b21b29ff94b759f20e94e4f7c06f424b0b4702e701c2a21668")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-scikit-build@0.15.0", type="build")
    depends_on("py-rapidfuzz-capi@1.0.5", type="build")
