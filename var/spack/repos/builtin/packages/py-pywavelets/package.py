# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPywavelets(PythonPackage):
    """PyWavelets is a free Open Source library for wavelet transforms
    in Python"""

    homepage = "https://github.com/PyWavelets/pywt"
    pypi = "PyWavelets/PyWavelets-0.5.2.tar.gz"

    license("MIT")

    version("1.4.1", sha256="6437af3ddf083118c26d8f97ab43b0724b956c9f958e9ea788659f6a2834ba93")
    version("1.1.1", sha256="1a64b40f6acb4ffbaccce0545d7fc641744f95351f62e4c6aaa40549326008c9")
    version("0.5.2", sha256="ce36e2f0648ea1781490b09515363f1f64446b0eac524603e5db5e180113bed9")

    depends_on("c", type="build")  # generated

    depends_on("python@3.8:", when="@1.4.1:", type=("build", "run"))
    depends_on("python@3.5:", when="@1.1.1:", type=("build", "run"))
    depends_on("py-setuptools@:64", type="build")
    depends_on("py-cython@0.29.24:2", when="@1.2:", type="build")
    depends_on("py-cython", type="build")

    depends_on("py-numpy@1.17.3:", when="@1.2:", type=("build", "run"))
    depends_on("py-numpy@1.13.3:", when="@1.1.1:", type=("build", "run"))
    depends_on("py-numpy@1.9.1:", type=("build", "run"))
    # https://github.com/PyWavelets/pywt/pull/731
    depends_on("py-numpy@:1", when="@:1.5", type=("build", "run"))
