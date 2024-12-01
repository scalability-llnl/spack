# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonLevenshtein(PythonPackage):
    """Python extension for computing string edit distances and
    similarities."""

    homepage = "https://github.com/ztane/python-Levenshtein"
    pypi = "python-Levenshtein/python-Levenshtein-0.12.0.tar.gz"

    license("GPL-2.0-or-later")

    version("0.12.0", sha256="033a11de5e3d19ea25c9302d11224e1a1898fe5abd23c61c7c360c25195e3eb1")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
