# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class CrosstoolNg(AutotoolsPackage):
    """Crosstool-NG is a versatile (cross) toolchain generator.

    It supports many architectures and components and has a simple yet powerful
    menuconfig-style interface.
    """

    homepage = "https://crosstool-ng.github.io/"
    url = "https://github.com/crosstool-ng/crosstool-ng/releases/download/crosstool-ng-1.25.0/crosstool-ng-1.25.0.tar.xz"

    maintainers("alalazo")

    version("1.26.0", sha256="e8ce69c5c8ca8d904e6923ccf86c53576761b9cf219e2e69235b139c8e1b74fc")
    version("1.25.0", sha256="68162f342243cd4189ed7c1f4e3bb1302caa3f2cbbf8331879bd01fe06c60cd3")

    depends_on("c", type="build")  # generated

    depends_on("ncurses")

    depends_on("bash", type=("build", "run"))
    depends_on("binutils", type=("build", "run"))
    depends_on("coreutils", type=("build", "run"))
    depends_on("elfutils~exeprefix", type=("build", "run"))
    depends_on("gawk", type=("build", "run"))
    depends_on("gmake", type=("build", "run"))
    depends_on("patch", type=("build", "run"))
    depends_on("sed", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"))

    depends_on("wget", type="run")
    depends_on("curl", type="run")

    depends_on("autoconf", type=("build", "run"))
    depends_on("automake", type=("build", "run"))
    depends_on("libtool", type=("build", "run"))

    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("grep", type="build")
    depends_on("help2man", type="build")
