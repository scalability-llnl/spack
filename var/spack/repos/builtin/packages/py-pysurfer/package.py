# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPysurfer(PythonPackage):
    """Cortical neuroimaging visualization in Python."""

    homepage = "https://github.com/nipy/PySurfer"
    pypi = "pysurfer/pysurfer-0.11.0.tar.gz"

    license("BSD-3-Clause")

    version("0.11.0", sha256="ae709b6f933694f1810eb3c8f517bdb76c13576d74a7a5a1704e05239df0a179")

    variant("save_movie", default=False, description="Enable save_movie support")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-nibabel@1.2:", type=("build", "run"))
    depends_on("py-mayavi", type=("build", "run"))

    depends_on("py-imageio@1.5:", when="+save_movie", type=("build", "run"))
