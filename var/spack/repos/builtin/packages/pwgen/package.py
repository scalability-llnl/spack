# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pwgen(AutotoolsPackage):
    """Pwgen is a small, GPL'ed password generator which creates passwords
    which can be easily memorized by a human."""

    homepage = "https://sourceforge.net/projects/pwgen/"
    url = "https://downloads.sourceforge.net/project/pwgen/pwgen/2.08/pwgen-2.08.tar.gz"

    maintainers("cessenat")

    license("GPL-2.0-only")

    version("2.08", sha256="dab03dd30ad5a58e578c5581241a6e87e184a18eb2c3b2e0fffa8a9cf105c97b")

    depends_on("c", type="build")  # generated

    depends_on("coreutils", type="build")
