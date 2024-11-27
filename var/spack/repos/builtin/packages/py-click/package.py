# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClick(PythonPackage):
    """Python composable command line interface toolkit."""

    homepage = "https://click.palletsprojects.com"
    pypi = "click/click-7.1.2.tar.gz"
    git = "https://github.com/pallets/click.git"

    license("BSD-3-Clause")

    version("8.1.7", sha256="ca9853ad459e787e2192211578cc907e7594e294c7ccc834310722b41b9ca6de")
    version("8.1.3", sha256="7682dc8afb30297001674575ea00d1814d808d6a36af415a82bd481d37ba7b8e")
    version("8.0.3", sha256="410e932b050f5eed773c4cda94de75971c89cdb3155a72a0831139a79e5ecb5b")
    version("8.0.1", sha256="8c04c11192119b1ef78ea049e0a6f0463e4c48ef00a30160c704337586f3ad7a")
    version("7.1.2", sha256="d2b5255c7c6349bc1bd1e59e08cd12acbbd63ce649f2588755783aa94dfb6b1a")
    version(
        "7.0",
        sha256="5b94b49521f6456670fdb30cd82a4eca9412788a93fa6dd6df72c94d5a8ff2d7",
        url="https://pypi.io/packages/source/c/click/Click-7.0.tar.gz",
    )
    version("6.6", sha256="cc6a19da8ebff6e7074f731447ef7e112bd23adf3de5c597cf9989f2fd8defe9")

    # Needed to ensure that Spack can bootstrap black with Python 3.6
    depends_on("python@3.7:", when="@8.1:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-importlib-metadata", when="@8: ^python@:3.7", type=("build", "run"))
    depends_on("py-colorama", when="@8: platform=windows", type=("build", "run"))
