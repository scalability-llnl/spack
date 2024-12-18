# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCvxpy(PythonPackage):
    """Convex optimization, for everyone."""

    homepage = "https://www.cvxpy.org/index.html"
    pypi = "cvxpy/cvxpy-1.0.25.tar.gz"

    license("Apache-2.0")

    version("1.1.13", sha256="a9c781e74ad76097b47b86456cb3a943898f7ec9ac8f47bcefc922051cdc4a04")
    version("1.0.25", sha256="8535529ddb807067b0d59661dce1d9a6ddb2a218398a38ea7772328ad8a6ea13")

    depends_on("cxx", type="build")  # generated

    # Dependency versions based on README.md in python packages
    depends_on("python@3.4:", type=("build", "run"), when="@1.1:")
    depends_on("python@3.6:", type=("build", "run"), when="@1.1.13:")
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.15:", type=("build", "run"))
    depends_on("py-scipy@1.1.0:", type=("build", "run"))
    depends_on("py-ecos@2:", type=("build", "run"))
    depends_on("py-scs@1.1.3:", type=("build", "run"))
    depends_on("py-scs@1.1.6:", type=("build", "run"), when="@1.1.13:")
    depends_on("py-osqp@0.4.1:", type=("build", "run"))
    depends_on("py-multiprocess", type=("build", "run"))
    depends_on("py-six", type=("build", "run"), when="@:1.0")
