# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyamg(PythonPackage):
    """PyAMG is a library of Algebraic Multigrid (AMG) solvers with
    a convenient Python interface."""

    homepage = "https://github.com/pyamg/pyamg"
    url = "https://github.com/pyamg/pyamg/archive/refs/tags/v4.0.0.zip"

    maintainers("benc303")

    license("MIT")

    version("5.0.0", sha256="088be4b38203e708905fa45295593c1336b127a28391486d4f5917cf0b96f5f2")
    version("4.2.3", sha256="dcf23808e0e8edf177fc4f71a6b36e0823ffb117137a33a9eee14b391ddbb733")
    version("4.1.0", sha256="9e340aef5da11280a1e28f28deeaac390f408e38ee0357d0fdbb77503747bbc4")
    version("4.0.0", sha256="015d5e706e6e54d3de82e05fdb173c30d8b27cb8a117ab584cd62ad41d9ea042")

    depends_on("python", type=("build", "link", "run"))
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-scipy@0.12:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build", when="@4.2.0:")
    # Later version required due to
    # https://github.com/pypa/setuptools_scm/issues/758
    depends_on("py-setuptools-scm@7.1:+toml", type="build", when="@5.0.0:")
    depends_on("py-setuptools-scm@5:+toml", type="build", when="@4.2.0:")
    depends_on("py-pybind11@2.8.0:", type=("build", "link"), when="@4.2.0:")
