# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pestpp(CMakePackage):
    """PEST++ is a software suite aimed at supporting complex numerical
    models in the decision-support context. Much focus has been devoted to
    supporting environmental models (groundwater, surface water, etc) but
    these tools are readily applicable to any computer model.
    """

    homepage = "https://pesthomepage.org"
    url = "https://github.com/usgs/pestpp/archive/5.0.5.tar.gz"

    version("5.2.9", sha256="401db5eec509c6771cd509a43c1710ac76b1ebe533f4cbaa1df26375aa167e60")
    version("5.2.3", sha256="6b86a7db863a034e730480046a4b7b4a8dc7cc798658a5404a961be379c05dc3")
    version("5.0.5", sha256="b9695724758f69c1199371608b01419973bd1475b1788039a2fab6313f6ed67c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI support")

    depends_on("cmake@3.9:", type="build")
    depends_on("mpi", type=("build", "run"), when="+mpi")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
