# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTypesSerialiser(PerlPackage):
    """Simple data types for common serialisation formats"""

    homepage = "https://metacpan.org/pod/Types::Serialiser"
    url = "https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/Types-Serialiser-1.01.tar.gz"

    maintainers("EbiArnie")

    version("1.01", sha256="f8c7173b0914d0e3d957282077b366f0c8c70256715eaef3298ff32b92388a80")

    depends_on("perl-common-sense", type=("build", "run", "test"))
