# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLineenhancer(PythonPackage):
    """The line enhancer is only used by crYOLO internally"""

    homepage = "https://github.com/MPI-Dortmund/LineEnhancer"
    pypi = "lineenhancer/lineenhancer-1.0.8.tar.gz"

    maintainers("dorton21")

    license("MIT")

    version("1.0.8", sha256="a1c7f2556110135d7298b0002674b669b8bbf23f94d63e3e3db8f17f2fd3efbe")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.14.5:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-mrcfile", type=("build", "run"))
