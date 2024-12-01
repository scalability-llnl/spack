# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNcTimeAxis(PythonPackage):
    """cftime support for matplotlib axis."""

    homepage = "https://github.com/scitools/nc-time-axis"
    pypi = "nc-time-axis/nc-time-axis-1.1.0.tar.gz"

    license("BSD-3-Clause")

    version("1.1.0", sha256="ea9d4f7f9e9189c96f7d320235ac6c4be7f63dc5aa256b3ee5d5cca5845e6e26")

    depends_on("py-setuptools", type="build")
    depends_on("py-cftime", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
