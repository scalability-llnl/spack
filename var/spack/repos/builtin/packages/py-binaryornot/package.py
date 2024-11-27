# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBinaryornot(PythonPackage):
    """Ultra-lightweight pure Python package to check if a file is binary or text."""

    homepage = "https://binaryornot.readthedocs.io"
    url = "https://github.com/audreyr/binaryornot/archive/0.4.0.tar.gz"

    license("BSD-3-Clause")

    version("0.4.4", sha256="8cca04876a5e9d01f0dda79390e99089da87f3c1948ab2720661ba379d1b23f2")

    depends_on("py-setuptools", type="build")
    depends_on("py-chardet")
