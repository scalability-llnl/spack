# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPystan(PythonPackage):
    """PyStan is a Python interface to Stan, a package for Bayesian inference."""

    homepage = "https://mc-stan.org/"
    pypi = "pystan/pystan-3.4.0.tar.gz"

    maintainers("haralmha")

    license("ISC")

    version("3.5.0", sha256="078571d071a5b7c0af59206d4994a0979f4ac4b61f4a720b640c44fe35514929")
    version("3.4.0", sha256="325e2fb0ab804555c05a603e0c9152ab11fcc3af01f3e9a9ff9fe9954b93184f")
    version("2.19.1.1", sha256="fa8bad8dbc0da22bbe6f36af56c9abbfcf10f92df8ce627d59a36bd8d25eb038")
    version("2.19.0.0", sha256="b85301b960d5991918b40bd64a4e9321813657a9fc028e0f39edce7220a309eb")

    # common requirements
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-poetry-core@1.0.0:", type=("build", "run"))

    # variable requirements
    depends_on("python@3.8:3", type=("build", "run"), when="@3.4.0:")
    depends_on("py-aiohttp@3.6:3", type=("build", "run"), when="@3.4.0:")
    depends_on("py-httpstan@4.8", type=("build", "run"), when="@3.5.0:")
    depends_on("py-httpstan@4.7", type=("build", "run"), when="@3.4")
    depends_on("py-pysimdjson@3.2:3", type=("build", "run"), when="@3.4.0:")
    depends_on("py-numpy@1.19:1", type=("build", "run"), when="@3.4.0:")
    depends_on("py-numpy@1.7:", type=("build", "run"), when="@2.19.0.0:")
    depends_on("py-clikit@0.6", type=("build", "run"), when="@3.4.0:")
    depends_on("py-cython@0.22:0.23.2,0.25.2:", type=("build", "run"), when="@:2.19.1.1")
