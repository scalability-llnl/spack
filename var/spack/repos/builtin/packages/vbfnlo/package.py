# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vbfnlo(AutotoolsPackage):
    """VBFNLO is a fully flexible parton level Monte Carlo program
    for the simulation of vector boson fusion, double and triple
    vector boson production in hadronic collisions at
    next to leading order in the strong coupling constant."""

    homepage = "https://www.itp.kit.edu/vbfnlo/wiki/doku.php?id=overview"
    url = "https://github.com/vbfnlo/vbfnlo/archive/v3.0.0beta5.tar.gz"

    tags = ["hep"]

    license("GPL-2.0-only")

    # The commented out versions exist, but are not tested
    version(
        "3.0.0beta5", sha256="777a3dedb365ea9abc38848a60f30d325da3799cbad69fa308664b94a8c31a90"
    )
    version(
        "3.0.0beta4", sha256="511e84765e9634a75766a160eae1925812dacbb3943e7e3b4dc90e2eacac8a2c"
    )
    # version('3.0.0beta3', sha256='ab4cc3289051ab09ed94fa41d0eb1c5c4adcd9f39fa04e3c95a3867f256541bc')
    version(
        "3.0.0beta2", sha256="33dd0781e645a5baa664fc5aa81d43c12586bf095ef25895e86cb4192c22473b"
    )
    version(
        "3.0.0beta1", sha256="19f0bf7e4c93b0f287d2531d6802c114a78eb46cde28ea820b2a074a5819c7ca"
    )
    version(
        "2.7.1",
        sha256="13e33d73d8a8ef64094621f87e6f94e01712e76cc19a86298d0b52cfcb9decca",
        preferred=True,
    )

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    # version('2.7.0',      sha256='0e96c0912599e3000fffec5305700b947b604a7b06c7975851503f445311e4ef')

    # Documentation is broken on some systems:
    # See https://github.com/vbfnlo/vbfnlo/issues/2
    variant("doc", default=False, description="Build documentation")

    depends_on("hepmc")
    depends_on("gsl")
    depends_on("lhapdf")
    depends_on("looptools")
    depends_on("automake", type="build")
    depends_on("autoconf", type="build")
    depends_on("m4", type="build")
    depends_on("libtool", type="build")

    @when("@2.7.1")
    def setup_build_environment(self, env):
        env.unset("F77")

    def configure_args(self):
        args = [
            "--with-hepmc=" + self.spec["hepmc"].prefix,
            "--with-gsl=" + self.spec["gsl"].prefix,
            "--with-LHAPDF=" + self.spec["lhapdf"].prefix,
            "--with-LOOPTOOLS=" + self.spec["looptools"].prefix,
            "FCFLAGS=-std=legacy",
        ]

        return args

    @when("@3.0.0beta3:~doc")
    def patch(self):
        filter_file("lib src doc", "lib src", "Makefile.am")
