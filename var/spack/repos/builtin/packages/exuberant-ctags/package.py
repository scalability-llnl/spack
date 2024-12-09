# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ExuberantCtags(AutotoolsPackage):
    """The canonical ctags generator"""

    homepage = "https://ctags.sourceforge.net"
    url = "https://downloads.sourceforge.net/project/ctags/ctags/5.8/ctags-5.8.tar.gz"

    license("GPL-2.0-or-later")

    version("5.8", sha256="0e44b45dcabe969e0bbbb11e30c246f81abe5d32012db37395eb57d66e9e99c7")

    depends_on("c", type="build")  # generated

    patch("ctags-5.8-gcc-unused-attribute.patch", when="@5.8")
