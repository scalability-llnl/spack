# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Termcap(AutotoolsPackage):
    """This is the GNU termcap library, a library of C functions that
    enable programs to send control strings to terminals in a way
    independent of the terminal type."""

    homepage = "https://www.gnu.org/software/termutils/manual/termcap-1.3/html_mono/termcap.html"
    url = "https://ftp.gnu.org/gnu/termcap/termcap-1.3.1.tar.gz"

    license("GPL-2.0-or-later")

    version("1.3.1", sha256="91a0e22e5387ca4467b5bcb18edf1c51b930262fd466d5fda396dd9d26719100")
    version("1.3", sha256="3eb4b98ae08408ca65dd9275f3c8e56e2feac1261fae914a9b21273db51cf000")

    depends_on("c", type="build")  # generated
