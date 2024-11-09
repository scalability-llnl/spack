# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRadicalGtod(PythonPackage):
    """RADICAL-GTOD provides a single method, gtod, which returns the current
    time in seconds since epoch (01.01.1970) with sub-second resolution and a
    binary tool, radical-gtod, which is a compiled binary and does not require
    the invocation of the Python interpreter."""

    homepage = "https://radical-cybertools.github.io"
    git = "https://github.com/radical-cybertools/radical.gtod.git"
    pypi = "radical.gtod/radical.gtod-1.47.0.tar.gz"

    maintainers("andre-merzky")

    license("LGPL-3.0-or-later")

    version("develop", branch="devel")
    version("1.47.0", sha256="52e75bf14faf352165ffa0d9e32ca472bd63f479020cd78f832baa34f8acfe6d")
    version("1.39.0", sha256="254f1e805b58a33b93c6180f018904db25538710ec9e75b3a3a9969d7206ecf6")

    version(
        "1.20.0",
        sha256="8d0846de7a5d094146c01fbb7c137f343e4da06af51efafeba79dd3fdfe421dc",
        deprecated=True,
    )
    version(
        "1.16.0",
        sha256="1fe9da598a965c7194ed9c7df49d5b30632a11a7f9ece12152bea9aaa91bd4b8",
        deprecated=True,
    )
    version(
        "1.13.0",
        sha256="15df4ae728a8878b111cfdedffb9457aecc8003c2cfbdf2c918dfcb6b836cc93",
        deprecated=True,
    )
    version(
        "1.6.7",
        sha256="8d7d32e3d0bcf6d7cf176454a9892a46919b03e1ed96bee389380e6d75d6eff8",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("py-radical-utils", type=("build", "run"), when="@1.13:")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
