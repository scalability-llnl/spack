# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOmegaconf(PythonPackage):
    """A hierarchical configuration system, with support for merging configurations from
    multiple sources (YAML config files, dataclasses/objects and CLI arguments)
    providing a consistent API regardless of how the configuration was created.
    """

    homepage = "https://github.com/omry/omegaconf"
    pypi = "omegaconf/omegaconf-2.3.0.tar.gz"

    maintainers("calebrob6")

    license("BSD-3-Clause")

    version("2.3.0", sha256="d5d4b6d29955cc50ad50c46dc269bcd92c6e00f5f90d23ab5fee7bfca4ba4cc7")
    version("2.2.2", sha256="10a89b5cb81887d68137b69a7c5c046a060e2239af4e37f20c3935ad2e5fd865")
    version("2.1.0", sha256="a08aec03a63c66449b550b85d70238f4dee9c6c4a0541d6a98845dcfeb12439d")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytest-runner", when="@2.1", type="build")
    depends_on("py-antlr4-python3-runtime@4.9", when="@2.2.2:", type=("build", "run"))
    depends_on("py-antlr4-python3-runtime@4.8", when="@2.1", type=("build", "run"))
    depends_on("py-pyyaml@5.1:", type=("build", "run"))
    depends_on("java", type="build")
