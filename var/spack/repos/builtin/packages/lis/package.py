# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lis(AutotoolsPackage):
    """Lis (Library of Iterative Solvers for linear systems,
    pronounced [lis]) is a parallel software library for
    solving discretized linear equations and eigenvalue
    problems that arise in the numerical solution of partial
    differential equations using iterative methods."""

    homepage = "https://www.ssisc.org/lis/index.en.html"
    url = "https://www.ssisc.org/lis/dl/lis-2.0.27.zip"

    version("2.1.7", sha256="cbcfca1dcd514801ef530ea5d158311985108ab6a9f300d31dcbd01d2175b4b2")
    version("2.1.6", sha256="7e2c4c5a1b96d2aa21fe799c073d7ca3cd5be79f350593d83102e37ca9780821")
    version("2.1.5", sha256="4b78335cf85c327976536b8ac584f258dc9ae085e91b5d4a40879422b3e71543")
    version("2.1.4", sha256="d94d634db49fff2368bb615225ee4fdde919c63b7a9bc1f81f7d166a8c105f92")
    version("2.1.3", sha256="2ca0682198c2cdb6beb7866bd2b25071dc8964c6f76d8962477f848f39ff57ea")
    version("2.1.2", sha256="673f01cb06446872f5a888e144b0d325d19444fea1e04c58e2ba8221ef645d46")
    version("2.1.1", sha256="e1b227fb9c88be4d897be4211198e1e9e8258eb75127848d35b67a0182bf4538")
    version("2.1.0", sha256="630a1341824fbeef7fdfb82413bfdeb7d3df14e77616ba88159fce1150cf006c")
    version("2.0.35", sha256="3b2d583f482b874b04a03cbfd7b432f4e558ad56023ccffc68bb5acdcdcafda7")
    version("2.0.34", sha256="f216593d92a93955d257857f863507333b48e24ad94fe614f0afb35c8edfda72")
    version("2.0.33", sha256="9c3a9294d640652dbe278bbac673ff7855a3785253b81cc2724d06b58a0b2285")
    version("2.0.32", sha256="93c515e1b38c9263d464f1c86773253a437fe973643618a6099fe0829e5c30d4")
    version("2.0.31", sha256="f04950e761e3def7104d94172c5357bffd21918e8f381ad4e0dcb6d596334031")
    version("2.0.30", sha256="fefe1ba48aa5867cde3c07ea4009fb333baa863b535a1f29bbdf99de42f49f67")
    version("2.0.29", sha256="aecf08f79595b3f1a888f153615f099fc2fcf6b90955ffbaba9cd01892d9614d")
    version("2.0.28", sha256="d2d8739ab11b605a62fca08fd56334c45ab10e7796a44f8243e1a1e3006fe36a")
    version("2.0.27", sha256="85f32f4abbc94d1b40b22c10b915170271b19822b6aa6939b1cb295f6e455237")

    variant("mpi", default=False, description="Build with MPI library")
    variant("omp", default=False, description="Build with openMP library")
    variant("f90", default=False, description="enable FORTRAN 90 compatible interfaces")

    depends_on("mpi", when="+mpi")

    def configure_args(self):
        config_args = []
        config_args.extend(self.enable_or_disable("mpi"))
        config_args.extend(self.enable_or_disable("omp"))
        config_args.extend(self.enable_or_disable("f90"))

        if self.spec.satisfies("%fj"):
            config_args.append("CLIBS=-lm")
            config_args.append("FCLDFLAGS=-mlcmain=main")

        return config_args
