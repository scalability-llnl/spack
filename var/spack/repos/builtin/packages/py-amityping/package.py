# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAmityping(PythonPackage):
    """Provides typing hints to be shared between LCLS-II analysis packages."""

    homepage = "https://github.com/slac-lcls/amityping"
    url = "https://github.com/slac-lcls/amityping/archive/refs/tags/1.1.12.tar.gz"

    maintainers("valmar")

    license("BSD-3-Clause-LBNL")

    version("1.1.12", sha256="e00e7102a53fa6ee343f018669f6b811d703a2da4728b497f80579bf89efbd3c")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-mypy-extensions", type=("build", "run"))
