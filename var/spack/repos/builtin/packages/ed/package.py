# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ed(AutotoolsPackage, GNUMirrorPackage):
    """GNU ed is a line-oriented text editor. It is used to create,
    display, modify and otherwise manipulate text files, both
    interactively and via shell scripts."""

    homepage = "https://www.gnu.org/software/ed"
    gnu_mirror_path = "ed/ed-1.4.tar.gz"

    license("GPL-2.0-or-later")

    version("1.4", sha256="db36da85ee1a9d8bafb4b041bd4c8c11becba0c43ec446353b67045de1634fda")

    depends_on("c", type="build")  # generated

    parallel = False
