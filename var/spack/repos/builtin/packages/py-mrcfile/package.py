# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMrcfile(PythonPackage):
    """Python implementation of the MRC2014 file format, which is used
    in structural biology to store image and volume data."""

    homepage = "https://github.com/ccpem/mrcfile/"
    url = "https://github.com/ccpem/mrcfile/archive/refs/tags/v1.3.0.tar.gz"

    maintainers("dorton21")

    license("BSD-3-Clause")

    version("1.4.3", sha256="0c2c702167c50c8b67e4ff7b1ec825a6bb60c0bff388950af08c79c5fd49e28b")
    version("1.3.0", sha256="034f1868abf87f4e494b8b039030b50045cabccf352b8b3e88a6bd3a6d665715")

    depends_on("python@3.4.0:")
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.16.0:", when="@1.4.3:", type=("build", "run"))
    depends_on("py-numpy@1.12.0:", when="@1.3.0", type=("build", "run"))
