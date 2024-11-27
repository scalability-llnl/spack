# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyOsqp(PythonPackage):
    """OSQP: The Operator Splitting QP Solver"""

    homepage = "https://osqp.org/"
    pypi = "osqp/osqp-0.6.1.tar.gz"

    maintainers("meyersbs")

    license("Apache-2.0")

    version(
        "0.6.2.post8", sha256="23d6bae4a3612f60d5f652d0e5fa4b2ead507cabfff5d930d822057ae6ed6677"
    )
    version("0.6.1", sha256="47b17996526d6ecdf35cfaead6e3e05d34bc2ad48bcb743153cefe555ecc0e8c")

    depends_on("c", type="build")  # generated

    depends_on("cmake", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@40.8.0:", when="@0.6.2.post8:", type="build")
    depends_on("py-setuptools-scm@6.2:", when="@0.6.2.post8:", type="build")
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-scipy@0.13.2:", type=("build", "run"))
    depends_on("py-future", when="@:0.6.1", type=("build", "run"))
    depends_on("py-qdldl", when="@0.6.2.post8:", type=("build", "run"))
