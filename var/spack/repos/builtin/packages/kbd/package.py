# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kbd(AutotoolsPackage):
    """The kbd project contains tools for managing Linux console
    (Linux console, virtual terminals, keyboard, etc.) - mainly,
    what they do is loading console fonts and keyboard maps."""

    homepage = "https://kbd-project.org/"
    url = "https://github.com/legionus/kbd/archive/v2.3.0.tar.gz"

    license("GPL-2.0-or-later")

    version("2.3.0", sha256="28f05450cfde08259341b9641d222027844c075f77a2bac6ce143b3f33a6eb4e")
    version("2.2.90", sha256="a310a915f474c85ee28cd860677a34a529aca940daa44634a428dd6df58c196e")
    version("2.2.0", sha256="5dec023c7a05b4d11d8ae795f59fab2b0bacfcc5c20a3d534dc7566cfe47ccf7")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("libpam")
