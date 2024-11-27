# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tig(AutotoolsPackage):
    """Text-mode interface for git"""

    homepage = "https://jonas.github.io/tig/"
    url = "https://github.com/jonas/tig/releases/download/tig-2.2.2/tig-2.2.2.tar.gz"

    license("GPL-2.0-or-later")

    version("2.5.10", sha256="f655cc1366fc10058a2bd505bb88ca78e653ff7526c1b81774c44b9d841210e3")
    version("2.5.8", sha256="b70e0a42aed74a4a3990ccfe35262305917175e3164330c0889bd70580406391")
    version("2.2.2", sha256="316214d87f7693abc0cbe8ebbb85decdf5e1b49d7ad760ac801af3dd73385e35")

    depends_on("c", type="build")  # generated

    depends_on("ncurses")
