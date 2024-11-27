# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Py4suiteXml(PythonPackage):
    """XML tools and libraries for Python: Domlette, XPath, XSLT, XPointer,
    XLink, XUpdate"""

    homepage = "http://4suite.org/"
    pypi = "4Suite-XML/4Suite-XML-1.0.2.tar.gz"

    version("1.0.2", sha256="f0c24132eb2567e64b33568abff29a780a2f0236154074d0b8f5262ce89d8c03")

    depends_on("c", type="build")  # generated

    depends_on("python@2.2.1:", type=("build", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
