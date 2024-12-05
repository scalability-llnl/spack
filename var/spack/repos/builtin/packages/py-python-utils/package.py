# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPythonUtils(PythonPackage):
    """Python Utils is a collection of small Python functions and classes
    which make common patterns shorter and easier."""

    homepage = "https://github.com/WoLpH/python-utils"
    pypi = "python-utils/python-utils-2.4.0.tar.gz"

    license("BSD-3-Clause")

    version("3.5.2", sha256="68198854fc276bc4b2403b261703c218e01ef564dcb072a7096ed9ea7aa5130c")
    version("2.7.1", sha256="88595bfa054975534a2f813b6c8deb96b44f3b6fad00a927fd062fe65550fadf")
    version("2.4.0", sha256="f21fc09ff58ea5ebd1fd2e8ef7f63e39d456336900f26bdc9334a03a3f7d8089")
    version("2.3.0", sha256="34aaf26b39b0b86628008f2ae0ac001b30e7986a8d303b61e1357dfcdad4f6d3")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", when="@:2.7.1", type=("build", "run"))

    depends_on("py-typing-extensions", when="@3.5.2 ^python@:3.7", type=("build", "run"))
