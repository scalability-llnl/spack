# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPytecplot(PythonPackage):
    """The pytecplot library is a high level API that connects your
    Python script to the power of the Tecplot 360 visualization engine.
    It offers line plotting, 2D and 3D surface plots in a variety of formats,
    and 3D volumetric visualization. Familiarity with Tecplot 360 and the
    Tecplot 360 macro language is helpful, but not required."""

    homepage = "https://www.tecplot.com/docs/pytecplot/"
    pypi = "pytecplot/pytecplot-1.4.2.zip"

    license("Frameworx-1.0")

    version("1.4.2", sha256="586a2ee947314ddd2f28be5523911dd298465b8f6a9145ba351866d5d695ef0d")

    variant("extras", default=False, description="Enable extra functionality.")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-flatbuffers", type=("build", "run"))
    depends_on("py-protobuf", type=("build", "run"))
    depends_on("py-pyzmq", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"), when="+extras")
    depends_on("py-ipython", type=("build", "run"), when="+extras")
    depends_on("py-pillow", type=("build", "run"), when="+extras")
    depends_on("tecplot@2017r1:", type=("build", "run"))
