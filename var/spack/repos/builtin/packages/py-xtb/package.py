# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXtb(PythonPackage):
    """Python API for the extended tight binding program package"""

    homepage = "https://xtb-python.readthedocs.org"
    pypi = "xtb/xtb-22.1.tar.gz"
    git = "https://github.com/grimme-lab/xtb-python.git"

    maintainers("awvwgk")

    license("LGPL-3.0-or-later")

    version("22.1", sha256="7a59e7b783fc6e8b7328f55211de681e535a83991b07c4bab73494063f5e9018")

    depends_on("pkgconfig", type="build")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-cffi", type=("build", "run"))
    depends_on("py-meson-python", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("xtb", type=("build", "run"))

    # from https://github.com/grimme-lab/xtb-python/pull/114
    patch(
        "https://github.com/grimme-lab/xtb-python/commit/df7e0010a679f5f00456bf09fcd9330cd7c56c39.patch?full_index=1",
        when="@:22.1",
        sha256="0242a4b79b7e24cfec3c0e6661e744eeb6a786d7",
    )
