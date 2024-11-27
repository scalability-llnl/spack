# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQdldl(PythonPackage):
    """Python interface to the QDLDL free LDL factorization routine for
    quasi-definite linear systems: Ax = b."""

    homepage = "https://github.com/oxfordcontrol/qdldl-python/"
    pypi = "qdldl/qdldl-0.1.5.post3.tar.gz"

    maintainers("meyersbs")

    license("Apache-2.0")

    version(
        "0.1.5.post3", sha256="69c092f6e1fc23fb779a80a62e6fcdfe2eba05c925860248c4d6754f4736938f"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools@18.0:", type="build")
    depends_on("py-pybind11", type="build")
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-scipy@0.13.2:", type=("build", "run"))
    depends_on("cmake", type="build")
