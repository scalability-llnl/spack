# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcppparallel(RPackage):
    """Parallel Programming Tools for 'Rcpp'.

    High level functions for parallel programming with 'Rcpp'. For example, the
    'parallelFor()' function can be used to convert the work of a standard
    serial "for" loop into a parallel one and the 'parallelReduce()' function
    can be used for accumulating aggregate or other values."""

    cran = "RcppParallel"

    version("5.1.9", sha256="fd0861f3f0f7be4e0ef29c021e75beb351ae2eb18ce5d79e21f2725da4da114f")
    version("5.1.7", sha256="f9c30eb9ce1abffc590825d513d6d28dcbe970e36032dd7521febf04e905b29c")
    version("5.1.5", sha256="6396322b3b6d6f7019aac808ceb74707bc5c4ed01677fab408372c2a5508c2ea")
    version("5.0.2", sha256="8ca200908c6365aafb2063be1789f0894969adc03c0f523c6cc45434b8236f81")
    version("4.4.3", sha256="7a04929ecab97e46c0b09fe5cdbac9d7bfa17ad7d111f1a9787a9997f45fa0fa")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("gmake", type="build")
    depends_on("tbb", when="@5.1.5:")

    patch("asclang.patch", when="%fj")
