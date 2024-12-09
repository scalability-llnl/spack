# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFastdtw(PythonPackage):
    """Python implementation of FastDTW
    (http://cs.fit.edu/~pkc/papers/tdm04.pdf), which is an approximate
    Dynamic Time Warping (DTW) algorithm that provides optimal or
    near-optimal alignments with an O(N) time and memory
    complexity."""

    homepage = "https://github.com/slaypni/fastdtw"
    pypi = "fastdtw/fastdtw-0.3.4.tar.gz"

    license("MIT")

    version("0.3.4", sha256="2350fa6ec36bcad186eaf81f46eff35181baf04e324f522de8aeb43d0243f64f")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-cython", type="build")
