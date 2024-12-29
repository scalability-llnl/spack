# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRx(PythonPackage):
    """Reactive Extensions (Rx) for Python"""

    homepage = "https://reactivex.io/"
    pypi = "Rx/Rx-3.2.0.tar.gz"

    maintainers("dorton21")

    version("3.2.0", sha256="b657ca2b45aa485da2f7dcfd09fac2e554f7ac51ff3c2f8f2ff962ecd963d91c")
    version("1.6.1", sha256="13a1d8d9e252625c173dc795471e614eadfe1cf40ffc684e08b8fff0d9748c23")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
