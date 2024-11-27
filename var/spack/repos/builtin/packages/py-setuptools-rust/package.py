# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetuptoolsRust(PythonPackage):
    """Setuptools rust extension plugin."""

    homepage = "https://github.com/PyO3/setuptools-rust"
    pypi = "setuptools-rust/setuptools-rust-0.12.1.tar.gz"

    license("MIT")

    version("1.9.0", sha256="704df0948f2e4cc60c2596ad6e840ea679f4f43e58ed4ad0c1857807240eab96")
    version("1.8.1", sha256="94b1dd5d5308b3138d5b933c3a2b55e6d6927d1a22632e509fcea9ddd0f7e486")
    version("1.7.0", sha256="c7100999948235a38ae7e555fe199aa66c253dc384b125f5d85473bf81eae3a3")
    version("1.6.0", sha256="c86e734deac330597998bfbc08da45187e6b27837e23bd91eadb320732392262")
    version("1.5.1", sha256="0e05e456645d59429cb1021370aede73c0760e9360bbfdaaefb5bced530eb9d7")
    version("1.4.1", sha256="18ff850831f58ee21d5783825c99fad632da21e47645e9427fd7dec048029e76")
    version("1.2.0", sha256="0a4ada479e8c7e3d8bd7cb56e1a29acc2b2bb98c2325051b0cdcb57d7f056de8")
    version("0.12.1", sha256="647009e924f0ae439c7f3e0141a184a69ad247ecb9044c511dabde232d3d570e")

    depends_on("py-setuptools@62.4:", when="@1.4.0:", type=("build", "run"))
    depends_on("py-setuptools@46.1:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", when="@1.7.0:", type=("build", "run"))
    depends_on("py-semantic-version@2.8.2:2", when="@1.2.0:", type=("build", "run"))
    depends_on("py-semantic-version@2.6.0:", type=("build", "run"))
    depends_on("py-tomli@1.2.1:", when="^python@:3.10", type=("build", "run"))
    depends_on("rust", type="run")

    # Historical dependencies
    depends_on("py-typing-extensions@3.7.4.3:", when="@1.2.0:1.7.0", type=("build", "run"))
    depends_on("py-setuptools-scm+toml@6.3.2:", when="@1.2.0:1.4.1", type="build")
    depends_on("py-setuptools-scm+toml@3.4.3:", when="@:1.1", type="build")
    depends_on("py-toml@0.9.0:", type=("build", "run"), when="@0.12.1")
