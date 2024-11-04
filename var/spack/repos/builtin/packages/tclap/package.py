# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tclap(AutotoolsPackage, SourceforgePackage):
    """Templatized C++ Command Line Parser"""

    homepage = "https://tclap.sourceforge.net"
    sourceforge_mirror_path = "tclap/tclap-1.2.2.tar.gz"

    license("MIT")

    version("1.2.5", sha256="bb649f76dae35e8d0dcba4b52acfd4e062d787e6a81b43f7a4b01275153165a6")
    version("1.2.4", sha256="634c5b59dbb1ccbc9d6a5f6de494a257e29a3f59dcb6fc30445ff39b45188574")
    version("1.2.3", sha256="19e7db5281540f154348770bc3a7484575f4f549aef8e00aabcc94b395f773c9")
    version("1.2.2", sha256="f5013be7fcaafc69ba0ce2d1710f693f61e9c336b6292ae4f57554f59fde5837")
    version("1.2.1", sha256="9f9f0fe3719e8a89d79b6ca30cf2d16620fba3db5b9610f9b51dd2cd033deebb")

    depends_on("cxx", type="build")  # generated
