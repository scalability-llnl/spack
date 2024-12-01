# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJunitXml(PythonPackage):
    """Creates JUnit XML test result documents that can be read by tools
    such as Jenkins"""

    homepage = "https://github.com/kyrus/python-junit-xml"
    pypi = "junit-xml/junit-xml-1.7.tar.gz"

    license("MIT")

    version("1.7", sha256="5bc851b53e3e2153dcc62278ce2aa796a8ae9208f1dec36d1507b5af445ce355")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
