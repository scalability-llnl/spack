# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGenomeinfodb(RPackage):
    """Utilities for manipulating chromosome names, including modifying them to
    follow a particular naming style.

    Contains data and functions that define and allow translation between
    different chromosome sequence naming conventions (e.g., "chr1" versus
    "1"), including a function that attempts to place sequence names in
    their natural, rather than lexicographic, order."""

    bioc = "GenomeInfoDb"

    version("1.36.0", commit="c380bb93a5480b48e0efbf6d107cefc10d574438")
    version("1.34.3", commit="ea6f131f1d1ee61535d6733ce76fabf3c62185fc")
    version("1.32.4", commit="69df6a5a10027fecf6a6d1c8298f3f686b990d8f")
    version("1.32.2", commit="2e40af38f00ee86d2c83d140e234c1349baa27de")
    version("1.30.1", commit="bf8b385a2ffcecf9b41e581794056f267895863d")
    version("1.26.2", commit="96dd27a7e3ef476790b1475aab50dbbed7df67a2")
    version("1.20.0", commit="ea771e3b429ef17fb912fb37333556c6f77f2265")
    version("1.18.2", commit="557b75ea7734749a2650d30f5c5d52c57a6bcc6f")
    version("1.16.0", commit="6543dad89bbc2c275010b329eb114b237fd712fa")
    version("1.14.0", commit="4978308a57d887b764cc4ce83724ca1758f580f6")
    version("1.12.3", commit="2deef3f0571b7f622483257bc22d2509ab5a0369")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@1.30.1:")
    depends_on("r-biocgenerics@0.13.8:", type=("build", "run"))
    depends_on("r-biocgenerics@0.37.0:", type=("build", "run"), when="@1.30.1:")
    depends_on("r-s4vectors@0.9.25:", type=("build", "run"))
    depends_on("r-s4vectors@0.17.25:", type=("build", "run"), when="@1.16.0:")
    depends_on("r-s4vectors@0.25.12:", type=("build", "run"), when="@1.26.2:")
    depends_on("r-iranges@1.99.26:", type=("build", "run"))
    depends_on("r-iranges@2.13.12:", type=("build", "run"), when="@1.16.0:")
    depends_on("r-rcurl", type=("build", "run"))
    depends_on("r-genomeinfodbdata", type=("build", "run"))
