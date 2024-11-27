# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Help2man(AutotoolsPackage, GNUMirrorPackage):
    """help2man produces simple manual pages from the '--help' and '--version'
    output of other commands."""

    homepage = "https://www.gnu.org/software/help2man/"
    gnu_mirror_path = "help2man/help2man-1.47.11.tar.xz"

    license("GPL-3.0-or-later")

    version("1.49.3", sha256="4d7e4fdef2eca6afe07a2682151cea78781e0a4e8f9622142d9f70c083a2fd4f")
    version("1.47.16", sha256="3ef8580c5b86e32ca092ce8de43df204f5e6f714b0cd32bc6237e6cd0f34a8f4")
    version("1.47.11", sha256="5985b257f86304c8791842c0c807a37541d0d6807ee973000cf8a3fe6ad47b88")
    version("1.47.8", sha256="528f6a81ad34cbc76aa7dce5a82f8b3d2078ef065271ab81fda033842018a8dc")
    version("1.47.4", sha256="d4ecf697d13f14dd1a78c5995f06459bff706fd1ce593d1c02d81667c0207753")

    depends_on("c", type="build")  # generated

    depends_on("perl", type=("build", "run"))
