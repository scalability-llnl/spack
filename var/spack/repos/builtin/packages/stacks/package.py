# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Stacks(AutotoolsPackage):
    """Stacks is a software pipeline for building loci from short-read
    sequences, such as those generated on the Illumina platform."""

    homepage = "https://catchenlab.life.illinois.edu/stacks/"
    url = "https://catchenlab.life.illinois.edu/stacks/source/stacks-1.46.tar.gz"

    license("GPL-3.0-or-later")

    version("2.53", sha256="ee1efceaeeeb7a39f0c2e804ad7c0a003094db28c9101120c38ddb02846e90fd")
    version("2.3b", sha256="a46786d8811a730ebcdc17891e89f50d4f4ae196734439dac86091f45c92ac72")
    version("1.46", sha256="45a0725483dc0c0856ad6b1f918e65d91c1f0fe7d8bf209f76b93f85c29ea28a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("sparsehash", default=True, description="Improve Stacks memory usage with SparseHash")

    depends_on("perl", type=("build", "run"))
    depends_on("sparsehash", when="+sparsehash")
    depends_on("zlib-api", when="@2.3b:")
    conflicts("%gcc@:4.9.0", when="@2.3b:")

    def configure_args(self):
        args = []
        if "+sparsehash" in self.spec:
            args.append("--enable-sparsehash")
        else:
            args.append("--disable-sparsehash")
        return args
