# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStackData(PythonPackage):
    """Extract data from python stack frames and tracebacks for informative
    displays."""

    homepage = "https://github.com/alexmojaki/stack_data"
    pypi = "stack_data/stack_data-0.2.0.tar.gz"

    license("MIT")

    version("0.6.2", sha256="32d2dd0376772d01b6cb9fc996f3c8b57a357089dec328ed4b6553d037eaf815")
    version("0.5.0", sha256="715c8855fbf5c43587b141e46cc9d9339cc0d1f8d6e0f98ed0d01c6cb974e29f")
    version("0.2.0", sha256="45692d41bd633a9503a5195552df22b583caf16f0b27c4e58c98d88c8b648e12")

    depends_on("py-setuptools@44:", type="build")
    depends_on("py-setuptools-scm+toml@3.4.3:", type="build")

    depends_on("py-executing@1.2:", when="@0.6:", type=("build", "run"))
    depends_on("py-executing", type=("build", "run"))
    depends_on("py-asttokens@2.1:", when="@0.6:", type=("build", "run"))
    depends_on("py-asttokens", type=("build", "run"))
    depends_on("py-pure-eval", type=("build", "run"))
