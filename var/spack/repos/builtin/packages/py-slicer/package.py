# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySlicer(PythonPackage):
    """slicer wraps tensor-like objects and provides a uniform slicing interface via __getitem__"""

    homepage = "https://github.com/interpretml/slicer"
    pypi = "slicer/slicer-0.0.7.tar.gz"

    version("0.0.7", sha256="f5d5f7b45f98d155b9c0ba6554fa9770c6b26d5793a3e77a1030fb56910ebeec")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.6:", type=("build", "run"))
