# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Discovar(AutotoolsPackage):
    """DISCOVAR is a variant caller and small genome assembler."""

    homepage = "https://software.broadinstitute.org/software/discovar/blog/"
    url = "ftp://ftp.broadinstitute.org/pub/crd/Discovar/latest_source_code/discovar-52488.tar.gz"

    license("MIT")

    version("52488", sha256="c46e8f5727b3c8116d715c02e20a83e6261c762e8964d00709abfb322a501d4e")

    depends_on("cxx", type="build")  # generated

    conflicts("%gcc@6:")
