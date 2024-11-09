# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import numbers

from spack.package import *
from spack.pkg.builtin.boost import Boost


def is_multiple_32(x):
    """multiple of 32"""
    try:
        return (
            isinstance(int(x), numbers.Integral) and not isinstance(x, bool) and int(x) % 32 == 0
        )
    except ValueError:
        return False


class Abyss(AutotoolsPackage):
    """ABySS is a de novo, parallel, paired-end sequence assembler
    that is designed for short reads. The single-processor version
    is useful for assembling genomes up to 100 Mbases in size."""

    homepage = "https://www.bcgsc.ca/platform/bioinfo/software/abyss"
    url = "https://github.com/bcgsc/abyss/releases/download/2.3.1/abyss-2.3.1.tar.gz"

    version("2.3.7", sha256="ba37780e79ec3aa359b6003e383caef13479a87f4d0022af01b86398f9ffca1f")
    version("2.3.5", sha256="5455f7708531681ee15ec4fd5620526a53c86d28f959e630dc495f526b7d40f7")
    version("2.3.1", sha256="664045e7903e9732411effc38edb9ebb1a0c1b7636c64b3a14a681f465f43677")
    version("2.3.0", sha256="3df923b0699187fb27948cae43293eeb5745161d5dc484b9befbe2ca8efb6ad7")
    version("2.2.5", sha256="38e886f455074c76b32dd549e94cc345f46cb1d33ab11ad3e8e1f5214fc65521")
    version("2.1.4", sha256="2145a1727556104d6a14db06a9c06f47b96c31cc5ac595ae9c92224349bdbcfc")
    version("2.0.2", sha256="d87b76edeac3a6fb48f24a1d63f243d8278a324c9a5eb29027b640f7089422df")
    version("1.5.2", sha256="8a52387f963afb7b63db4c9b81c053ed83956ea0a3981edcad554a895adf84b1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "maxk", default=128, values=is_multiple_32, description="set the maximum k-mer length."
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("bwa", type="run")

    depends_on("mpi")
    depends_on("boost@:1.50.0,1.53.0:", when="@2.0.2:")
    depends_on("boost@:1.50.0,1.53.0:1.59.0", when="@:1.5.2")
    # Maintainers: Is boost really a dependency? In what conditions?
    depends_on(Boost.with_default_variants)
    depends_on("sparsehash")
    depends_on("sqlite")
    depends_on("libtool")

    conflicts("^intel-mpi")
    conflicts("^intel-parallel-studio+mpi")
    conflicts("^mvapich2")
    conflicts("^spectrum-mpi")

    def configure_args(self):
        maxk = int(self.spec.variants["maxk"].value)
        args = [
            f"--with-boost={self.spec['boost'].prefix}",
            f"--with-sqlite={self.spec['sqlite'].prefix}",
            f"--with-mpi={self.spec['mpi'].prefix}",
        ]
        if maxk:
            args.append(f"--enable-maxk={maxk}")
        if self.spec["mpi"].name == "mpich":
            args.append("--enable-mpich")
        return args

    patch("fix_BloomFilter.hpp.patch", when="@2.0.0:2.1.4")
