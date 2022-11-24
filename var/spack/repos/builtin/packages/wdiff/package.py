# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Wdiff(AutotoolsPackage, GNUMirrorPackage):
    """GNU word-wise diff tools"""

    homepage = "https://www.gnu.org/software/wdiff/"
    url = "http://ftp.gnu.org/gnu/wdiff/wdiff-1.2.2.tar.gz"

    version(
        "1.2.2",
        sha256="34ff698c870c87e6e47a838eeaaae729fa73349139fc8db12211d2a22b78af6b",
    )

    depends_on("ncurses")
