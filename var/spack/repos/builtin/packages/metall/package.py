# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Metall(CMakePackage):
    """A Persistent Memory Allocator For Data-Centric Analytics"""

    homepage = "https://github.com/LLNL/metall"
    git = "https://github.com/LLNL/metall.git"
    url = "https://github.com/LLNL/metall/archive/refs/tags/v0.20.tar.gz"

    maintainers("KIwabuchi", "rogerpearce", "mayagokhale")

    tags = ["e4s"]

    license("MIT")

    version("master", branch="master")
    version("develop", branch="develop")

    version("0.28", sha256="770dedb7f8220c333688b232a22104ca9d8d5823e7a8a21152b58ef970eb85d0")
    version("0.27", sha256="6e6f17a760778f9162def939701f9381a75e5275fd1eb1b2af4b2e89e86e1c58")
    version("0.26", sha256="7453c87d99708be8542e354e582cbeefac1e5ba65e609cd85d7126c5b25a6d7b")
    version("0.25", sha256="223cb54543b62a62fdbbe6274b02ddcc14b29806e344ee7e2fd3f055c2374295")
    version("0.24", sha256="872de2a1b76d44e6876c0b672c0cc518c6f334959e4a229f2f18cc7e01edf477")
    version("0.23.1", sha256="25e8fbc424e66d09e0faf60029288e4612685675bfd947cc142bd9d6d0645ac4")
    version("0.23", sha256="17987922a3eb23a6b904498858db94aca12859d5dbcd8483704619ae93353340")
    version("0.22", sha256="e937fcb667902b2a578eaad65a44aa4107f63cdede135ead5ef48bb889ed13ad")
    version("0.21", sha256="feaff7a935f98d3cc1e2b21f6eae40edc674a5bd0133306afd3851148aaed026")
    version("0.20", sha256="cafe54c682004a66a059f54e2d7128ea7622e9941ea492297d04c260675e9af4")
    version("0.19", sha256="541f428d4a7e629e1e60754f9d5f5e84fe973d421b2647f5ed2ec25b977ddd56")
    version("0.18", sha256="cd1fee376d0523d43e43b92c43731d45a2c4324278a071a5f626f400afecef24")
    version("0.17", sha256="8de6ec2a430a141a2ad465ccd40ba9d0eb0c57d9f2f2de657fe837a73c466e61")
    version("0.16", sha256="190fa6936cbbfad1844659eb1fcfd1ad8c5880f60e76e223e33c506d371ea3a3")
    version("0.15", sha256="a1ea475ce1297b0c4cdf450544dc60ecf1b0a30c548b08ba77ccda5585df7248")
    version("0.14", sha256="386a6db0cfd3b3693cf8b0de323dcb60d43777aa5c871b744c9e8c19a572a917")
    version("0.13", sha256="959d37d0a7e7e5b4d5e6c0334aaaeef1b463e855fa8e807042f662c993ed60b1")
    version("0.12", sha256="b757b354b355e866bd6d42da53b0160442f3b7f663a19ba113da1ffc1a76176e")
    version("0.11", sha256="7cfa6a7eaaeb7fd11ecfbe43a172a36c8cde200601d6cd3b309d7a0acf752f3c")
    version("0.10", sha256="58b4b5507d4db5baca315b1bed2b728981755d755b91ef63bd0b6dfaf320f46b")
    version("0.9", sha256="2d7bd9ea2f1e04136050f210884445a9e3dcb96c992cf42ff9ea4b392f85f927")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.12:", type="build")
    depends_on("boost@1.75:", type=("build", "link"))

    # googletest is required only for test
    # GCC is also required only for test (Metall is a header-only library)
    # Hint: Use 'spack install --test=root metall' or 'spack install --test=all metall'
    # to run test (adds a call to 'make test' to the build)
    depends_on("googletest %gcc@8.1.0:", type=("test"))

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, type=("build", "link"))

    def cmake_args(self):
        if self.run_tests:
            args = ["-DBUILD_TEST=ON", "-DSKIP_DOWNLOAD_GTEST=ON"]
            return args
        else:
            args = ["-DINSTALL_HEADER_ONLY=ON"]
            return args

    def setup_build_environment(self, env):
        # Configure the directories for test
        if self.run_tests:
            env.set("METALL_TEST_DIR", join_path(self.build_directory, "build_test"))

    # 'spack load metall' sets METALL_ROOT environmental variable
    def setup_run_environment(self, env):
        env.set("METALL_ROOT", self.prefix)
