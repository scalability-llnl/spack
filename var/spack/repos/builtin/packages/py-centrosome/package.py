# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCentrosome(PythonPackage):
    """An open source image processing library."""

    homepage = "https://github.com/CellProfiler/centrosome"
    pypi = "centrosome/centrosome-1.2.2.tar.gz"

    maintainers("omsai")

    license("BSD-3-Clause", checked_by="omsai")

    version("1.2.2", sha256="4b38181d6648cb8b0e896aa2e54b5a6da2e9ebc19a8110582307f5c6da9d9964")

    depends_on("python@2.7:,3.5:", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("py-deprecation", type=("build", "run"))
    depends_on("py-matplotlib@3.1.3:", type=("build", "run"))
    depends_on("py-numpy@1.18.2:", type=("build", "run"))
    depends_on("py-pillow@7.1:", type=("build", "run"))
    depends_on("py-scikit-image@0.17.2:", type=("build", "run"))
    depends_on("py-scipy@1.4.1:1.10", type=("build", "run"))
