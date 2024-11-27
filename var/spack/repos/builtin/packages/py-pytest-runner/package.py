# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestRunner(PythonPackage):
    """Invoke py.test as distutils command with dependency resolution."""

    homepage = "https://github.com/pytest-dev/pytest-runner"
    pypi = "pytest-runner/pytest-runner-5.1.tar.gz"

    license("MIT")

    version("6.0.0", sha256="b4d85362ed29b4c348678de797df438f0f0509497ddb8c647096c02a6d87b685")
    version("5.3.1", sha256="0fce5b8dc68760f353979d99fdd6b3ad46330b6b1837e2077a89ebcf204aac91")
    version("5.1", sha256="25a013c8d84f0ca60bb01bd11913a3bcab420f601f0f236de4423074af656e7a")
    version("2.11.1", sha256="983a31eab45e375240e250161a556163bc8d250edaba97960909338c273a89b3")

    # requirements from pyproject.toml are marked with *
    depends_on("python@3.6:", when="@5.3:", type=("build", "run"))
    depends_on("python@3.7:", when="@6.0.0:", type=("build", "run"))
    depends_on("py-setuptools@56:", when="@6.0.0:", type=("build", "run"))  # *
    depends_on("py-setuptools@42:", when="@5.3:", type=("build", "run"))  # *
    depends_on("py-setuptools@34.4:", when="@5:", type=("build", "run"))  # *
    depends_on("py-setuptools@27.3:", when="@4.1:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm+toml@3.4.1:", when="@5.3:", type="build")  # *
    depends_on("py-setuptools-scm@1.15:", type="build")
