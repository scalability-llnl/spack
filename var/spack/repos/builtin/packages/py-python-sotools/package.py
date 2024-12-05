# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonSotools(PythonPackage):
    """python-sotools is a collection of tools to work with ELF shared objects"""

    pypi = "python-sotools/python-sotools-0.1.0.tar.gz"

    license("BSD-3-Clause")

    version("0.1.0", sha256="39a088f2ca384294e19a96a82d883feb729f0f2e5ae21d9785be357124ec61f2")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyelftools", type=("build", "run"))
