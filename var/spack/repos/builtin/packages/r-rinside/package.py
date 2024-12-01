# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRinside(RPackage):
    """C++ Classes to Embed R in C++ (and C) Applications.

    C++ classes to embed R in C++ applications The 'RInside' packages makes it
    easier to have "R inside" your C++ application by providing a C++
    wrapperclass providing the R interpreter. As R itself is embedded into your
    application, a shared library build of R is required. This works on Linux,
    OS X and even on Windows provided you use the same tools used to build R
    itself. Numerous examples are provided in the eight subdirectories of the
    examples/ directory of the installed package: standard, mpi (for parallel
    computing) qt (showing how to embed 'RInside' inside a Qt GUI application),
    wt (showing how to build a "web-application" using the Wt toolkit),
    armadillo (for 'RInside' use with 'RcppArmadillo') and eigen (for 'RInside'
    use with 'RcppEigen'). The example use GNUmakefile(s) with GNU extensions,
    so a GNU make is required (and will use the GNUmakefile automatically).
    Doxygen-generated documentation of the C++ classes is available at the
    'RInside' website as well."""

    cran = "RInside"

    version("0.2.18", sha256="805014f0f0a364633e0e3c59100665a089bc455dec80b24f04aaec96466cb736")
    version("0.2.17", sha256="0be28c44ee34cba669a7264d2b99c289230645598ca78e21682559dc31824348")
    version("0.2.16", sha256="7ae4ade128ea05f37068d59e610822ff0b277f9d39d8900f7eb31759ad5a2a0e")
    version("0.2.15", sha256="1e1d87a3584961f3aa4ca6acd4d2f3cda26abdab027ff5be2fd5cd76a98af02b")
    version("0.2.14", sha256="8de5340993fe879ca00fa559c5b1b27b408ba78bfc5f67d36d6f0b8d8e8649cf")
    version("0.2.13", sha256="be1da861f4f8c1292f0691bce05978e409a081f24ad6006ae173a6a89aa4d031")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r-rcpp", type=("build", "run"))
