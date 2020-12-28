# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tclap(AutotoolsPackage, SourceforgePackage):
    """Templatized C++ Command Line Parser"""

    homepage = "http://tclap.sourceforge.net"
    sourceforge_mirror_path = "tclap/tclap-1.2.2.tar.gz"

    version('1.2.2', sha256='f5013be7fcaafc69ba0ce2d1710f693f61e9c336b6292ae4f57554f59fde5837')
    version('1.2.1', sha256='9f9f0fe3719e8a89d79b6ca30cf2d16620fba3db5b9610f9b51dd2cd033deebb')
