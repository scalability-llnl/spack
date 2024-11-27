# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBagit(PythonPackage):
    """bagit is a Python library and command line utility
    for working with BagIt style packages.
    """

    homepage = "https://libraryofcongress.github.io/bagit-python"
    pypi = "bagit/bagit-1.8.1.tar.gz"

    license("CC0-1.0")

    version("1.8.1", sha256="37df1330d2e8640c8dee8ab6d0073ac701f0614d25f5252f9e05263409cee60c")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
