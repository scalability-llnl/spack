# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Discovardenovo(AutotoolsPackage):
    """DISCOVAR de novo is a large (and small) de novo genome assembler.
    It quickly generates highly accurate and complete assemblies using the
    same single library data as used by DISCOVAR. It currently doesn't
    support variant calling, for that, please use DISCOVAR instead."""

    homepage = "https://software.broadinstitute.org/software/discovar/blog/"
    url = "ftp://ftp.broadinstitute.org/pub/crd/DiscovarDeNovo/latest_source_code/discovardenovo-52488.tar.gz"

    license("MIT")

    version("52488", sha256="445445a3b75e17e276a6119434f13784a5a661a9c7277f5e10f3b6b3b8ac5771")

    depends_on("cxx", type="build")  # generated

    # lots of compiler errors with GCC7, works with 4.8.5
    # and devs claim it works with 4.7 so I'm assuming 4.7-4.8'll work
    conflicts("%gcc@5:")
    conflicts("%gcc@:4.7.0")

    depends_on("samtools")
    depends_on("jemalloc")
