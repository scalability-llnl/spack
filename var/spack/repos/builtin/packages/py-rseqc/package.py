# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRseqc(PythonPackage):
    """RSeQC package provides a number of useful modules that can
    comprehensively evaluate high throughput sequence data especially RNA-seq
    data."""

    homepage = "https://rseqc.sourceforge.net"
    pypi = "RSeQC/RSeQC-2.6.4.tar.gz"

    version("5.0.1", sha256="3c7d458784861af352d8da3f4f1cc8941934b37643164e9b74f929a32bd9ca80")
    version("4.0.1", sha256="6a16a3c56b73917082d3ac060a113c7d32cccf39f86efa87a6f1e6b52642210d")
    version("3.0.1", sha256="d5f4cb2c24a7348929f5c4947d84c5869e8cd2cba5ba5248d991ebb37c4c6b3d")

    depends_on("py-setuptools", type="build")
    depends_on("py-nose@0.10.4:", type="build")
    depends_on("py-cython@0.17:", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))
    depends_on("py-bx-python", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pybigwig", type=("build", "run"))

    depends_on("r", type="run")
