# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchFancyPypiReadme(PythonPackage):
    """Fancy PyPI READMEs with Hatch."""

    homepage = "https://github.com/hynek/hatch-fancy-pypi-readme"
    pypi = "hatch_fancy_pypi_readme/hatch_fancy_pypi_readme-22.7.0.tar.gz"

    version("23.1.0", sha256="b1df44063094af1e8248ceacd47a92c9cf313d6b9823bf66af8a927c3960287d")
    version("22.7.0", sha256="dedf2ba0b81a2975abb1deee9310b2eb85d22380fda0d52869e760b5435aa596")

    depends_on("py-hatchling", type=("build", "run"))
    depends_on("py-tomli", when="^python@:3.10", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))
