# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRoifile(PythonPackage):
    """Roifile is a Python library to read, write, create, and plot ImageJ ROIs"""

    homepage = "https://www.cgohlke.com/"
    pypi = "roifile/roifile-2024.1.10.tar.gz"

    license("BSD-3-Clause", checked_by="A-N-Other")

    version("2024.1.10", sha256="8bbc05a96c0a291429214cb6829426378e89931d1a7d3ad945aa2fea5765e434")

    variant("all", default=True, description="Enable TIFF support")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))

    depends_on("py-matplotlib", type=("build", "run"), when="+all")
    depends_on("py-tifffile", type=("build", "run"), when="+all")
