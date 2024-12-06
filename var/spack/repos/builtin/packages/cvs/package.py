# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Cvs(AutotoolsPackage, GNUMirrorPackage):
    """CVS a very traditional source control system"""

    homepage = "https://www.nongnu.org/cvs/"
    gnu_mirror_path = "non-gnu/cvs/source/feature/1.12.13/cvs-1.12.13.tar.bz2"

    license("GPL-2.0-or-later")

    version("1.12.13", sha256="78853613b9a6873a30e1cc2417f738c330e75f887afdaf7b3d0800cb19ca515e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # To avoid the problem: The use of %n in format strings in writable memory
    # may crash the program on glibc2 systems from 2004-10-18 or newer.
    patch(
        "https://gentoofan.org/gentoo/poly-c_overlay/dev-vcs/cvs/files/cvs-1.12.13.1-fix-gnulib-SEGV-vasnprintf.patch",
        sha256="e13db2acebad3ca5be5d8e0fa97f149b0f9661e4a9a731965c8226290c6413c0",
        when="@1.12.13",
    )

    tags = ["build-tools"]

    parallel = False
    executables = [r"^cvs$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"\(CVS\)\s+([\d\.]+)", output)
        return match.group(1) if match else None
