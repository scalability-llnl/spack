# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyInheritance(PythonPackage):
    """This module is a general-purpose framework for evaluating if a
    family exihibits, for example, and autosomal dominant pattern.
    """

    homepage = "https://github.com/brentp/inheritance"
    url = "https://github.com/brentp/inheritance/archive/v0.1.5.tar.gz"

    license("MIT")

    version("0.1.5", sha256="d0621328649a636a42766488fbd0d36d7fb898429120fc579d656711147a0c7c")
    version("0.1.3", sha256="c12e668ff3d34d9544b0eb4a58e7ba94f265d610545bb151e330ec014a07fda6")

    depends_on("python", type=("build", "run"))
    depends_on("py-setuptools", type="build")
