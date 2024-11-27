# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIniparse(PythonPackage):
    """Accessing and Modifying INI files"""

    homepage = "https://github.com/candlepin/python-iniparse"
    pypi = "iniparse/iniparse-0.4.tar.gz"
    git = "https://github.com/candlepin/python-iniparse.git"

    license("MIT")

    version("master", branch="master")

    depends_on("python@2.6:2.8,3.3:", when="@master:", type=("build", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
