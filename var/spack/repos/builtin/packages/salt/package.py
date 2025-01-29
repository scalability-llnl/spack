# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Salt(CMakePackage):
    """SALT: A next generation LLVM-based Source Analysis Toolkit for performance instrumentation of HPC applications"""

    homepage = "https://github.com/ParaToolsInc/salt"
    url = "https://github.com/ParaToolsInc/salt/archive/refs/tags/v0.2.0.tar.gz"
    git = "https://github.com/ParaToolsInc/salt.git"

    maintainers("zbeekman", "wspear")

    license("Apache-2.0", checked_by="wspear")

    version("master", branch="master")
    version("0.2.0", sha256="55c80f9d0591752b1e5b40e924718dc28f928ee0a3c7008adec3feab1280c57f")

    depends_on("llvm+clang+flang@19:")
