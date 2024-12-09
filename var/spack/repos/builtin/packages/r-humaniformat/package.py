# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHumaniformat(RPackage):
    """A Parser for Human Names

    Human names are complicated and nonstandard things. Humaniformat, which is
    based on Anthony Ettinger's 'humanparser' project
    (https://github.com/chovy/humanparser) provides functions for parsing human
    names, making a best- guess attempt to distinguish sub-components such as
    prefixes, suffixes, middle names and salutations."""

    homepage = "https://github.com/Ironholds/humaniformat"
    cran = "humaniformat"

    maintainers("jgaeb")

    license("MIT")

    version("0.6.0", sha256="861232c66bf6d4ff91b073193506104f4d99eca5e9a9488327f39ef2bfb45e6d")
    version("0.5.0", sha256="02b585e3623a5c5faa7dc3abff92b932d748900be39097c5db8434b8e92709a0")

    depends_on("cxx", type="build")  # generated

    depends_on("r-rcpp", type=("build", "run"))
