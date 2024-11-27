# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmd(AutotoolsPackage):
    """This library provides message digest functions found on BSD systems
    either on their libc (NetBSD, OpenBSD) or libmd (FreeBSD, DragonflyBSD,
    macOS, Solaris) libraries and lacking on others like GNU systems."""

    homepage = "https://www.hadrons.org/software/libmd/"
    url = "https://archive.hadrons.org/software/libmd/libmd-1.0.3.tar.xz"

    maintainers("haampie")

    version("1.0.4", sha256="f51c921042e34beddeded4b75557656559cf5b1f2448033b4c1eec11c07e530f")
    version("1.0.3", sha256="5a02097f95cc250a3f1001865e4dbba5f1d15554120f95693c0541923c52af4a")
    version("1.0.2", sha256="dc66b8278f82e7e1bf774fbd4bc83a0348e8f27afa185b2c2779cfcb3da25013")
    version("1.0.1", sha256="e14eeb931cf85330f95ff822262d3033125488dfb2f867441e36e2d2c4a34c71")
    version("1.0.0", sha256="f21aea69f6411cb4307cda1f6378c7ed07830202b5f4cb9e64f681fdaf2d64c7")

    depends_on("c", type="build")  # generated

    # Use wrapper functions instead of __attribute__ __alias__
    patch("nvhpc-aliases.patch", when="%nvhpc")
