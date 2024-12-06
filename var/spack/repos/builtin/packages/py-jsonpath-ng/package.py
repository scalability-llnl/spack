# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJsonpathNg(PythonPackage):
    """A final implementation of JSONPath for Python that aims to be
    standard compliant, including arithmetic and binary comparison
    operators."""

    homepage = "https://github.com/h2non/jsonpath-ng"
    pypi = "jsonpath-ng/jsonpath-ng-1.5.2.tar.gz"

    license("Apache-2.0")

    version("1.6.0", sha256="5483f8e9d74c39c9abfab554c070ae783c1c8cbadf5df60d561bc705ac68a07e")
    version("1.5.3", sha256="a273b182a82c1256daab86a313b937059261b5c5f8c4fa3fc38b882b344dd567")
    version("1.5.2", sha256="144d91379be14d9019f51973bd647719c877bfc07dc6f3f5068895765950c69d")

    depends_on("py-setuptools", type="build")
    depends_on("py-ply", type=("build", "run"))
    depends_on("py-decorator", type=("build", "run"), when="@:1.5")
    depends_on("py-six", type=("build", "run"), when="@:1.5")
