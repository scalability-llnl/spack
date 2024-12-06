# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydeprecate(PythonPackage):
    """Simple tooling for marking deprecated functions or classes and re-routing
    to the new successors' instance."""

    homepage = "https://borda.github.io/pyDeprecate/"
    pypi = "pyDeprecate/pyDeprecate-0.3.0.tar.gz"

    license("MIT")

    version("0.3.1", sha256="fa26870924d3475621c344045c2c01a16ba034113a902600c78e75b3fac5f72c")
    version("0.3.0", sha256="335742ec53b9d22a0a9ff4f3470300c94935f6e169c74b08aee14d871ca40e00")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
