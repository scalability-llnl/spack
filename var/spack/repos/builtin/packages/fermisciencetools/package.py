# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fermisciencetools(Package):
    """The Fermi Science Tools consists of the basic tools necessary to
    analyze Fermi data.

    This is the binary version for Linux x86_64 with libc-2.17."""

    homepage = "https://fermi.gsfc.nasa.gov/ssc/data/analysis/software/"
    url = "https://fermi.gsfc.nasa.gov/ssc/data/analysis/software/v11r5p3/ScienceTools-v11r5p3-fssc-20180124-x86_64-unknown-linux-gnu-libc2.17.tar.gz"

    # Now we are using the binary distribution. The source distribution is also
    # available, but there might be some logical errors in the configure codes,
    # which leads to failing in building it from source. Hopefully someone else
    # can figure it out and we can use the source distribution instead.
    version("11r5p3", sha256="2f4fc32a0b2e5c0f1ddb220a0560f67e66052b7907c72dba181908dc9269ffe8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    def install(self, spec, prefix):
        install_tree("x86_64-unknown-linux-gnu-libc2.17", prefix)
