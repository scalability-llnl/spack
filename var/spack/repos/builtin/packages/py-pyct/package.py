# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyct(PythonPackage):
    """Python package common tasks for users (e.g. copy examples, fetch data, ...)"""

    pypi = "pyct/pyct-0.4.8.tar.gz"

    maintainers("vvolkl")

    license("BSD-3-Clause")

    version("0.4.8", sha256="23d7525b5a1567535c093aea4b9c33809415aa5f018dd77f6eb738b1226df6f7")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools@30.3.0:", type="build")
    depends_on("py-param@1.7.0:", type=("build", "run"))
