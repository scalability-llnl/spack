# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJproperties(PythonPackage):
    """Java Property file parser and writer for Python"""

    homepage = "https://github.com/Tblue/python-jproperties"
    pypi = "jproperties/jproperties-2.1.1.tar.gz"

    maintainers("teaguesterling")

    license("BSD", checked_by="teaguesterling")

    version("2.1.1", sha256="40b71124e8d257e8954899a91cd2d5c0f72e0f67f1b72048a5ba264567604f29")
    version("2.1.0", sha256="504d7b8d3b2f5f0f52c22c1f72bd50576dca17b01b4cd00d4359c6b0607a59ce")
    version("2.0.0", sha256="b6709652f5c602e5271f519cf14cb9bf5d5a101df06e6c1d300123477a239588")
    version("1.0.1", sha256="327e14082653a4f2212ff81a96fbf141382f727f421e8afc933bf56ff7c010f4")

    depends_on("py-setuptools", type="build")
    with default_args(type=("build", "run")):
        depends_on("python@2.7,3:")
        depends_on("py-six@1.10:1", when="@2.0.0")
        depends_on("py-six@1.12:1", when="@2.1.0")
        depends_on("py-six@1.13:1", when="@2.1.1")
        depends_on("py-setuptools-scm@3.3:3", when="@2.1.1")
