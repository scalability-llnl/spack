# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AllpathsLg(AutotoolsPackage):
    """ALLPATHS-LG is our original short read assembler and it works on both
    small and large (mammalian size) genomes."""

    homepage = "https://www.broadinstitute.org/software/allpaths-lg/blog/"
    url = "ftp://ftp.broadinstitute.org/pub/crd/ALLPATHS/Release-LG/latest_source_code/allpathslg-52488.tar.gz"

    version("52488", sha256="035b49cb21b871a6b111976757d7aee9c2513dd51af04678f33375e620998542")

    depends_on("cxx", type="build")  # generated

    # compiles with gcc 4.7.0 to 4.9.4)
    conflicts("%gcc@:4.6.4,5.1.0:")
    conflicts("%cce")
    conflicts("%apple-clang")
    conflicts("%clang")
    conflicts("%intel")
    conflicts("%nag")
    conflicts("%pgi")
    conflicts("%xl")
    conflicts("%xl_r")
