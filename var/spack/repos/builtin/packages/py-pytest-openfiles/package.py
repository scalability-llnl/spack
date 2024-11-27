# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytestOpenfiles(PythonPackage):
    """A plugin for the pytest framework that allows developers to detect
    whether any file handles or other file-like objects were inadvertently
    left open at the end of a unit test"""

    homepage = "https://github.com/astropy/pytest-openfiles"
    pypi = "pytest-openfiles/pytest-openfiles-0.5.0.tar.gz"

    license("BSD-3-Clause")

    version("0.5.0", sha256="179c2911d8aee3441fee051aba08e0d9b4dab61b829ae4811906d5c49a3b0a58")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@30.3.1:", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-pytest@4.6:", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
