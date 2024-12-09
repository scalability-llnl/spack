# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sandbox(AutotoolsPackage):
    """sandbox'd LD_PRELOAD hack by Gentoo Linux"""

    homepage = "https://www.gentoo.org/proj/en/portage/sandbox/"
    url = "https://dev.gentoo.org/~mgorny/dist/sandbox-2.12.tar.xz"

    license("GPL-2.0-or-later")

    version("2.25", sha256="24055986a1ed9b933da608e41e3284ee53c5a724f3c2457009f8e09e9c581ca8")
    version("2.12", sha256="265a490a8c528237c55ad26dfd7f62336fa5727c82358fc9cfbaa2e52c47fc50")

    depends_on("c", type="build")  # generated

    depends_on("gawk", type="build")
