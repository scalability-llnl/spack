# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlit(PythonPackage):
    """Flit is a simple way to put Python packages and modules on PyPI."""

    homepage = "https://github.com/pypa/flit"
    pypi = "flit/flit-3.9.0.tar.gz"
    maintainers("takluyver")

    license("BSD-3-Clause")

    version("3.9.0", sha256="d75edf5eb324da20d53570a6a6f87f51e606eee8384925cd66a90611140844c7")
    version("3.8.0", sha256="d0f2a8f4bd45dc794befbf5839ecc0fd3830d65a57bd52b5997542fac5d5e937")
    version("3.7.1", sha256="3c9bd9c140515bfe62dd938c6610d10d6efb9e35cc647fc614fe5fb3a5036682")
    version("3.6.0", sha256="b1464e006df4df4c8eeb37671c0e0ce66e1d04e4a36d91b702f180a25fde3c11")
    version("3.3.0", sha256="65fbe22aaa7f880b776b20814bd80b0afbf91d1f95b17235b608aa256325ce57")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-flit-core@3.9.0:3", when="@3.9.0:3", type=("build", "run"))
    depends_on("py-flit-core@3.8.0:3", when="@3.8.0:3.8", type=("build", "run"))
    depends_on("py-flit-core@3.7.1:3", when="@3.7.1:3.7", type=("build", "run"))
    depends_on("py-flit-core@3.6.0:3", when="@3.6.0:3.6", type=("build", "run"))
    depends_on("py-flit-core@3.3.0:3", when="@3.3.0:3.3", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-docutils", type=("build", "run"))
    depends_on("py-tomli", when="@3.4:3.7", type=("build", "run"))
    depends_on("py-tomli-w", when="@3.4:", type=("build", "run"))
    depends_on("py-toml", when="@3.3.0:3.3", type=("build", "run"))
