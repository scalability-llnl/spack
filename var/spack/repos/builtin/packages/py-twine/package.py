# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTwine(PythonPackage):
    """Twine is a utility for publishing Python packages on PyPI."""

    homepage = "https://twine.readthedocs.io/"
    pypi = "twine/twine-2.0.0.tar.gz"
    git = "https://github.com/pypa/twine.git"

    version("4.0.2", sha256="9e102ef5fdd5a20661eb88fad46338806c3bd32cf1db729603fe3697b1bc83c8")
    version("4.0.1", sha256="96b1cf12f7ae611a4a40b6ae8e9570215daff0611828f5fe1f37a16255ab24a0")
    version("2.0.0", sha256="9fe7091715c7576df166df8ef6654e61bada39571783f2fd415bdcba867c6993")

    depends_on("py-setuptools@45:", when="@3.4.1:", type="build")
    depends_on("py-setuptools@0.7.0:", type="build")
    depends_on("py-setuptools-scm+toml@6:", when="@3.4.2:", type="build")

    depends_on("py-pkginfo@1.8.1:", when="@3.7:", type=("build", "run"))
    depends_on("py-pkginfo@1.4.2:", type=("build", "run"))
    depends_on("py-readme-renderer@35:", when="@4.0.1:", type=("build", "run"))
    depends_on("py-readme-renderer@21.0:", type=("build", "run"))
    depends_on("py-requests@2.20:", type=("build", "run"))
    depends_on("py-requests-toolbelt@0.8.0:0.8,0.9.1:", type=("build", "run"))
    depends_on("py-urllib3@1.26:", when="@3.8:", type=("build", "run"))
    depends_on("py-importlib-metadata@3.6:", when="@3.4:", type=("build", "run"))
    depends_on("py-keyring@15.1:", when="@3:", type=("build", "run"))
    depends_on("py-rfc3986@1.4:", when="@3.2:", type=("build", "run"))
    depends_on("py-rich@12:", when="@4:", type=("build", "run"))

    # Historical Dependencies
    depends_on("py-tqdm@4.14:", when="@:3", type=("build", "run"))
