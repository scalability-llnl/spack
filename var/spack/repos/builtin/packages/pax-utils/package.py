# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PaxUtils(AutotoolsPackage):
    """ELF utils that can check files for security relevant properties"""

    homepage = "https://wiki.gentoo.org/index.php?title=Project:Hardened/PaX_Utilities"
    url = "https://dev.gentoo.org/~vapier/dist/pax-utils-1.2.2.tar.xz"

    license("GPL-2.0-only")

    version("1.3.3", sha256="eeca7fbd98bc66bead4a77000c2025d9f17ea8201b84245882406ce00b9b6b14")
    version("1.2.2", sha256="7f4a7f8db6b4743adde7582fa48992ad01776796fcde030683732f56221337d9")

    depends_on("c", type="build")  # generated
