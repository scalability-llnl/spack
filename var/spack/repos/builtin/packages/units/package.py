# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Units(AutotoolsPackage, GNUMirrorPackage):
    """GNU units converts between different systems of units"""

    homepage = "https://www.gnu.org/software/units/"
    gnu_mirror_path = "units/units-2.13.tar.gz"

    license("GPL-3.0-only")

    version("2.23", sha256="d957b451245925c9e614c4513397449630eaf92bd62b8495ba09bbe351a17370")
    version("2.22", sha256="5d13e1207721fe7726d906ba1d92dc0eddaa9fc26759ed22e3b8d1a793125848")
    version("2.13", sha256="0ba5403111f8e5ea22be7d51ab74c8ccb576dc30ddfbf18a46cb51f9139790ab")

    depends_on("c", type="build")  # generated

    depends_on("python", type=("build", "run"))
