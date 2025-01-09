# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Adept(AutotoolsPackage):
    """Combined array and automatic differentiation library in C++."""

    homepage = "https://www.met.reading.ac.uk/clouds/adept/"
    url = "https://www.met.reading.ac.uk/clouds/adept/adept-2.1.1.tar.gz"

    maintainers("jehicken")

    license("Apache-2.0", checked_by="jehicken")

    version("2.1.1", sha256="0cef334e82df4526d3761bdd8319a63e7582c96b2f1cc88391729018b4825c47")

    variant("blas", default=False, description="Enable Adept's native arrays using Openblas")
    variant("lapack", default=False, description="Enable Adept's native arrays using Lapack")

    depends_on("cxx", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("openblas", when="+blas")
    depends_on("netlib-lapack", when="+lapack")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = []

        if self.spec.satisfies("+blas"):
            blas_prefix = self.spec["openblas"].prefix
            args.append(f"--with-blas={blas_prefix}")

        if self.spec.satisfies("+lapack"):
            lapack_prefix = self.spec["netlib-lapack"].prefix
            args.append(f"--with-lapack={lapack_prefix}")

        return args
