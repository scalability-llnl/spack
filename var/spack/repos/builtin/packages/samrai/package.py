# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Samrai(AutotoolsPackage):
    """SAMRAI (Structured Adaptive Mesh Refinement Application Infrastructure)
    is an object-oriented C++ software library enables exploration of
    numerical, algorithmic, parallel computing, and software issues
    associated with applying structured adaptive mesh refinement
    (SAMR) technology in large-scale parallel application development.

    """

    homepage = "https://computing.llnl.gov/projects/samrai"
    url = "https://computing.llnl.gov/projects/samrai/download/SAMRAI-v3.11.2.tar.gz"
    list_url = homepage
    tags = ["radiuss"]

    version("3.12.0", sha256="b8334aa22330a7c858e09e000dfc62abbfa3c449212b4993ec3c4035bed6b832")
    version("3.11.5", sha256="6ec1f4cf2735284fe41f74073c4f1be87d92184d79401011411be3c0671bd84c")
    version("3.11.4", sha256="fa87f6cc1cb3b3c4856bc3f4d7162b1f9705a200b68a5dc173484f7a71c7ea0a")
    # Version 3.11.3 permissions don't allow downloading
    version("3.11.2", sha256="fd9518cc9fd8c8f6cdd681484c6eb42114aebf2a6ba4c8e1f12b34a148dfdefb")
    version("3.11.1", sha256="14317938e55cb7dc3eca21d9b7667a256a08661c6da988334f7af566a015b327")
    version("3.10.0", sha256="8d6958867f7165396459f4556e439065bc2cd2464bcfe16195a2a68345d56ea7")
    version("3.9.1", sha256="ce0aa9bcb3accbd39c09dd32cbc9884dc00e7a8d53782ba46b8fe7d7d60fc03f")
    version("3.8.0", sha256="0fc811ca83bd72d238f0efb172d466e80e5091db0b78ad00ab6b93331a1fe489")
    version("3.7.3", sha256="19eada4f351a821abccac0779fde85e2ad18b931b6a8110510a4c21707c2f5ce")
    version("3.7.2", sha256="c20c5b12576b73a1a095d8ef54536c4424517adaf472d55d48e57455eda74f2d")
    version(
        "3.6.3-beta", sha256="7d9202355a66b8850333484862627f73ea3d7620ca84cde757dee629ebcb61bb"
    )
    version(
        "3.5.2-beta", sha256="9a591fc962edd56ea073abd13d03027bd530f1e61df595fae42dd9a7f8b9cc3a"
    )
    version(
        "3.5.0-beta", sha256="3e10c55d7b652b6feca902ce782751d4b16c8ad9d4dd8b9e2e9ec74dd64f30da"
    )
    version(
        "3.4.1-beta", sha256="5aadc813b75b65485f221372e174a2691e184e380f569129e7aa4484ca4047f8"
    )
    version(
        "3.3.3-beta", sha256="c07b5dc8d56a8f310239d1ec6be31182a6463fea787a0e10b54a3df479979cac"
    )
    version(
        "3.3.2-beta", sha256="430ea1a77083c8990a3c996572ed15663d9b31c0f8b614537bd7065abd6f375f"
    )
    version("2.4.4", sha256="33242e38e6f4d35bd52f4194bd99a014485b0f3458b268902f69f6c02b35ee5c")

    # Debug mode reduces optimization, includes assertions, debug symbols
    # and more print statements
    variant(
        "debug", default=False, description="Compile with reduced optimization and debugging on"
    )
    variant("silo", default=False, description="Compile with support for silo")
    variant("shared", default=False, description="Build shared libraries")

    depends_on("mpi")
    depends_on("zlib-api")
    depends_on("hdf5+mpi")
    depends_on("m4", type="build")
    depends_on("boost@:1.64.0", when="@3.0.0:3.11", type="build")
    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="@3.0.0:3.11.99", type="build")
    depends_on("silo+mpi", when="+silo")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    # don't build SAMRAI 3+ with tools with gcc
    patch("no-tool-build.patch", when="@3.0.0:%gcc")

    # 2.4.4 needs a lot of patches to fix ADL and performance problems
    patch(
        "https://github.com/IBAMR/IBAMR/releases/download/v0.3.0/ibamr-samrai-fixes.patch?full_index=1",
        sha256="1d088b6cca41377747fa0ae8970440c20cb68988bbc34f9032d5a4e6aceede47",
        when="@2.4.4",
    )

    def configure_args(self):
        options = []

        options.extend(
            [
                "--with-CXX=%s" % self.spec["mpi"].mpicxx,
                "--with-CC=%s" % self.spec["mpi"].mpicc,
                "--with-F77=%s" % self.spec["mpi"].mpifc,
                "--with-M4=%s" % self.spec["m4"].prefix,
                "--with-hdf5=%s" % self.spec["hdf5"].prefix,
                "--with-zlib=%s" % self.spec["zlib-api"].prefix,
                "--without-blas",
                "--without-lapack",
                "--with-hypre=no",
                "--with-petsc=no",
            ]
        )

        # SAMRAI 2 used templates; enable implicit instantiation
        if self.spec.satisfies("@:3"):
            options.append("--enable-implicit-template-instantiation")

        if "+debug" in self.spec:
            options.extend(["--disable-opt", "--enable-debug"])
        else:
            options.extend(["--enable-opt", "--disable-debug"])

        if "+silo" in self.spec:
            options.append("--with-silo=%s" % self.spec["silo"].prefix)

        if "+shared" in self.spec:
            options.append("--enable-shared")

        if self.spec.satisfies("@3.0:3.11"):
            options.append("--with-boost=%s" % self.spec["boost"].prefix)

        return options

    def setup_dependent_build_environment(self, env, dependent_spec):
        if self.spec.satisfies("@3.12:"):
            env.append_flags("CXXFLAGS", self.compiler.cxx11_flag)
