# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCinemaLib(PythonPackage):
    """cinema_lib is a set of tools and library for interacting with a
    Cinema database (currently Spec A and Spec D) through Python and
    the command line tool, cinema."""

    homepage = "https://cinemascience.github.io/"
    url = "https://github.com/cinemascience/cinema_lib/archive/1.2.1.tar.gz"
    git = "https://github.com/cinemascience/cinema_lib.git"

    maintainers("EthanS94")

    version("master", branch="master")
    version("1.2.1", sha256="13c6c7b3df7dae3e05c2f44009b7c149841f604b7c51f36067bbcea9e2d088eb")
    version("1.2.0", sha256="f76b55517b7cfe7311d953426e08ce364b2e7e1cf84699828c229dd068ee3a08")
    version("1.1.1", sha256="90001554b0f3207d57da9fcab768732449d89a9d5bf54cfe0928a76649caebe8")
    version("1.1.0", sha256="2bd1787106643fd533e899a7e1b0f57f3933cde8c907e762f38ca95ac10316fd")
    version("1.0.2", sha256="3ebe52546e1325bd23732cd171146dbb2a9e0c25ac616224bf6f8fff9e8d48b1")
    version("1.0.1", sha256="5c2d220aa1dc28aec18f73c5cf0c4be3c834fffa0580e85b07050ff46364095d")
    version("1.0.0", sha256="9e2967fd22f1b1324ca2579df6501d0bfbc5fb142ca41c7a02f9b7d109767d3c")
    version(
        "ECPMilestone201806",
        sha256="dfb7b1d0e3d8d1865814622879ddb019c2a16efb947201832a56a98186ff46ce",
    )

    variant(
        "image", default=True, description="Enable image-processing algorithms from scikit-image"
    )
    variant("opencv", default=False, description="Enable computer vision algorithms from OpenCV")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-numpy@1.13:", when="+image", type=("build", "run"))
    depends_on("py-numpy@1.13:", when="+opencv", type=("build", "run"))
    depends_on("py-scikit-image@0.13.1:", when="+image", type=("build", "run"))
    depends_on("opencv@3.4:+python3", when="+opencv", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
