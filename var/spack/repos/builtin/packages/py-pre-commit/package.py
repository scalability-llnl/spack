# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPreCommit(PythonPackage):
    """A framework for managing and maintaining multi-language pre-commit
    hooks."""

    homepage = "https://github.com/pre-commit/pre-commit"
    pypi = "pre_commit/pre_commit-1.20.0.tar.gz"

    license("MIT")

    version("3.6.0", sha256="d30bad9abf165f7785c15a21a1f46da7d0677cb00ee7ff4c579fd38922efe15d")
    version("3.5.0", sha256="5804465c675b659b0862f07907f96295d490822a450c4c40e747d0b1c6ebcb32")
    version("3.3.3", sha256="a2256f489cd913d575c145132ae196fe335da32d91a8294b7afe6622335dd023")
    version("2.20.0", sha256="a978dac7bc9ec0bcee55c18a277d553b0f419d259dadb4b9418ff2d00eb43959")
    version("2.17.0", sha256="c1a8040ff15ad3d648c70cc3e55b93e4d2d5b687320955505587fd79bbaed06a")
    version("2.10.1", sha256="399baf78f13f4de82a29b649afd74bef2c4e28eb4f021661fc7f29246e8c7a3a")
    version("1.20.0", sha256="9f152687127ec90642a2cc3e4d9e1e6240c4eb153615cb02aa1ad41d331cbb6e")

    depends_on("python@3.9:", when="@3.6:", type=("build", "run"))
    depends_on("python@3.8:", when="@3:", type=("build", "run"))
    depends_on("python@3.7:", when="@2.20.0:", type=("build", "run"))
    depends_on("python@3.6.1:", when="@2.1.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-cfgv@2:", type=("build", "run"))
    depends_on("py-identify@1:", type=("build", "run"))
    depends_on("py-nodeenv@0.11.1:", type=("build", "run"))
    depends_on("py-pyyaml@5.1:", when="@2.1:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-virtualenv@20.10:", when="@2.21:", type=("build", "run"))
    depends_on("py-virtualenv@20.0.8:", when="@2.4:", type=("build", "run"))
    depends_on("py-virtualenv@15.2:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-toml", when="@:2.20", type=("build", "run"))
    depends_on("py-aspy-yaml", when="@1", type=("build", "run"))
    depends_on("py-six", when="@1", type=("build", "run"))
    depends_on("py-importlib-metadata", when="@:2 ^python@:3.7", type=("build", "run"))
