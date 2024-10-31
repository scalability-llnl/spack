# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyQutip(PythonPackage):
    """QuTiP: The Quantum Toolbox in Python"""

    homepage = "https://qutip.org/"
    pypi = "qutip/qutip-4.7.0.tar.gz"

    license("BSD-3-Clause")

    version("4.7.1", sha256="9a87178e68b145c2145b526caa943ccc8400a111325ced45bd17f9b893663af2")
    version("4.7.0", sha256="a9dde64457991ef1c5a7d4186b5348a16a71480a610f1c0902e4d656ddc12e31")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-packaging", type=("build", "run"))

    depends_on("py-cython@0.29.20:", type="build")
    depends_on("py-numpy@1.16.6:", type=("build", "run"))
    # https://github.com/qutip/qutip/pull/2421
    depends_on("py-numpy@:1", type=("build", "run"))
    depends_on("py-scipy@1.0:", type=("build", "run"))
