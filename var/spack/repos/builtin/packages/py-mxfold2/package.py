# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMxfold2(PythonPackage):
    """MXfold2: RNA secondary structure prediction using deep
    learning with thermodynamic integration"""

    homepage = "https://github.com/keio-bioinformatics/mxfold2"
    url = "https://github.com/keio-bioinformatics/mxfold2/releases/download/v0.1.1/mxfold2-0.1.1.tar.gz"

    maintainers("dorton21")

    license("MIT")

    version("0.1.1", sha256="9f39c6ff4138212d1ad2639005f5c05ffb4df0f7e22f5e7ad49466a05aa047e5")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-torch@1.7:~valgrind", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))
    depends_on("py-wheel@0.35.1:0.36.0", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-cpp", type="build")
    depends_on("cmake", type="build")
