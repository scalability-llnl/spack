# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libvori(CMakePackage):
    """Support for Voronoi Integration and lossless BQB compression"""

    homepage = "https://brehm-research.de/voronoi.php"
    url = "https://www.cp2k.org/static/downloads/libvori-201217.tar.gz"

    maintainers("dev-zero", "mtaillefumier")

    license("LGPL-3.0-only")

    version("220621", sha256="1cfa98c564814bddacf1c0e7f11582137d758668f6307e6eb392c72317984c14")
    version("210412", sha256="331886aea9d093d8c44b95a07fab13d47f101b1f94a0640d7d670eb722bf90ac")
    version("201229", sha256="da0afb292c94f8de2aaebfd0b692d15ffd86083cb8a48478b07ca93823decc06")
    version("201224", sha256="16f6c49eaa17ea23868925dbaae2eca71bdacbe50418c97d6c55e05728038f31")
    version("201217", sha256="6ad456ed6ca5d28cadcc0d90eabe8fff5caa77b99f12764323de5e3ae21cddf5")

    depends_on("cxx", type="build")  # generated

    variant("pic", default=True, description="Compile the library with position independent code")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic")]
        return args
