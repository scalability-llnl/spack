# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Thepeg(AutotoolsPackage):
    """Toolkit for High Energy Physics Event Generation"""

    homepage = "http://home.thep.lu.se/~leif/ThePEG/"
    url = "https://thepeg.hepforge.org/downloads/?f=ThePEG-2.2.1.tar.bz2"

    tags = ["hep"]

    license("GPL-3.0-or-later")

    # The commented out versions exist, but may need patches
    # and/or recipe changes
    version("2.3.0", sha256="ac35979ae89c29608ca92c156a49ff68aace7a5a12a0c92f0a01a833d2d34572")
    version("2.2.3", sha256="f21473197a761fc32917b08a8d24d2bfaf93ff57f3441fd605da99ac9de5d50b")
    version("2.2.2", sha256="97bf55d4391b0a070a3303d3845f8160afec403f1573dfb0e857709ad6262e3e")
    version("2.2.1", sha256="63abc7215e6ad45c11cf9dac013738e194cc38556a8368b850b70ab1b57ea58f")
    version("2.2.0", sha256="d3e1474811b7d9f61a4a98db1e9d60d8ef8f913a50de4cae4dc2cc4f98e6fbf8")
    # version('2.1.7', sha256='2e15727afc1fbfb158fa42ded31c4b1e5b51c25ed6bb66a38233e1fc594329c8')
    version("2.1.6", sha256="c1e51f83716bfca815b55100fbab3805ef5f9b9215e4373b22762693f5353f4f")
    version("2.1.5", sha256="c61a00fb6cf406f0f98e8c934683d8d5efcb655747842113abc92e9526e4b5e6")
    # version('2.1.4', sha256='400c37319aa967ed993fdbec84fc65b24f6cb3779fb1b173d7f5d7a56b772df5')
    version("2.1.3", sha256="16e8f6507530c2b80ed873ad22946efefed7355d15c7026f3465f18acebc1c0c")
    # version('2.1.2', sha256='6a0f675a27e10863d495de069f25b892e532beb32e9cbfe5a58317d015387f49')
    version("2.1.1", sha256="e1b0bdc116fbc9a6e598b601f2aa670530cf2e1cd46b4572814a9b0130b10281")
    # version('2.1.0', sha256='fe6e7740ce3cd4a3ce3d7a0079a16c9214ad18f432e29d034ae763bfc40f3d39')
    # version('2.0.4', sha256='f3b625b411667e2708995f1d1379b5b8691406853c8c2cca2f4e4e6e062da0e4')
    # version('2.0.3', sha256='c57ba68fbfda06a0ba256e06f276f91434bf2529a13f6287c051a4cd6da44634')
    # version('2.0.2', sha256='d4249e019543d5c7520733292d2edfb0bdd9733177200a63837781ed6194789b')
    # version('2.0.1', sha256='ec284abdc82ceaf10a8736f908e7955f49f872b79aaa62d22aa33bc5c7679bdb')
    # version('2.0.0', sha256='571730cc956027dc82780dc04ef6e7382ab5ea853fcfebe259e488c6df302a04')
    version("1.9.2", sha256="ff7bbb256866f994dae04ade1f57c92d2670edaac3df11c9a300419a5343faf4")
    # version('1.9.1', sha256='8ec6d0669eba51e308be4e33aeb219999418170eae3aad93ec1491c942c2a4e9')
    version("1.9.0", sha256="3ee58e5e3a26184567df1b9a10ca70df228e86f322e72f018dd7d8d5a4700a5d")
    version("1.8.3", sha256="55ede3a3dd0bd07b90d0d49cf7ae28c18cd965780fdf53528508b97d57152fc7")

    depends_on("cxx", type="build")  # generated
    # version('1.8.2', sha256='44ccd0d70e42bb6ecd801a51bade6c25b3953c56f33017402d4f52ee6492dffa')
    # version('1.8.1', sha256='84c2a212a681545cddd541dca191eb65d96f41df86c87480b6f4f7d4f9683562')
    # version('1.8.0', sha256='4b22fda1078f410b999a23a17f611c9ae3a7f0f4cee4e83dc82c9336b7adf037')
    # version('1.7.3', sha256='066d5df74118d6e984bb60e1c0bea08a8edcbcf917d83d8bc32ec6fea0726187')
    # version('1.7.2', sha256='3b885c6c5a39b7399ccd45d1f5a866b7a65c96174a56a7ff4ae423347843d013')
    # version('1.7.1', sha256='13434dc7a8623cacb94c0b5c8d7e15b4c5d5187fe9322d1afc1c91b2c940102e')
    # version('1.7.0', sha256='40eb7196139a8bf4c35f5bb69818135943d534457df64aeb1cf60b6621435312')
    # version('1.6.1', sha256='5bc074b78f8b663a6a33df9c94dcaa3100269f8da59f9553a565298e55af270f')
    # version('1.6.0', sha256='c0ac06b70f3e8046fce4e49ba5916c9b49450f528d0e25f8f7f1427c62fec680')
    # version('1.5.0', sha256='ccbf102cf1d350a21487518d12e7e03e6e50010e5604f0201f256fa46a7a50c2')
    # version('1.4.2', sha256='40444304e40e07fd417a8ebf8e5c1cf07e895ceac52ef4f7c1eecc911f6f775c')
    # version('1.4.1', sha256='156d06fd1ce68466d1f2adb9cc13f412b8b87073ec6a1d02102b173c34c29b8a')
    # version('1.4.0', sha256='b1f55e9a3bec713e9abf2fe71c5bd8cf8df936ea00b09f96df9123d0d5ab233f')
    # version('1.3.0', sha256='f731ebf3ce5a52b6d750d6e3c282fdc74d8ffd78bccb47b68f10a4daf44c7045')

    patch("thepeg-1.8.3.patch", when="@1.8.3", level=0)
    patch("thepeg-1.9.0.patch", when="@1.9.0", level=0)
    patch("thepeg-1.9.2.patch", when="@1.9.2", level=0)
    patch("thepeg-2.1.1.patch", when="@2.1.1:2.2.1", level=0)

    force_autoreconf = True

    depends_on("gsl")
    depends_on("lhapdf")
    depends_on("lhapdf@:6.2", when="@:1.9")
    depends_on("hepmc", when="hepmc=2")
    depends_on("hepmc3", when="hepmc=3")
    conflicts("hepmc=3", when="@:2.1", msg="HepMC3 support was added in 2.2.0")
    depends_on("fastjet", when="@2.0.0:")
    depends_on("rivet", when="@2.0.3: +rivet")
    depends_on("boost +test", when="@2.1.1:")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("zlib-api")

    variant("hepmc", default="2", values=("2", "3"), description="HepMC interface to build ")
    variant("rivet", default=True, description="Add rivet integration")
    variant(
        "libs",
        default="shared",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )

    install_targets = ["install-strip"]

    def flag_handler(self, name, flags):
        if name in ("cxxflags", "cflags", "fflags", "cppflags"):
            flags.append("-O2")

        return (None, None, flags)

    def configure_args(self):
        args = ["--with-gsl=" + self.spec["gsl"].prefix, "--without-javagui"]
        args += ["--with-zlib=" + self.spec["zlib-api"].prefix]

        if self.spec.satisfies("@:1.8"):
            args += ["--with-LHAPDF=" + self.spec["lhapdf"].prefix]
        else:
            args += ["--with-lhapdf=" + self.spec["lhapdf"].prefix]

        if self.spec.satisfies("hepmc=2"):
            args += ["--with-hepmc=" + self.spec["hepmc"].prefix]
        else:
            args += ["--with-hepmc=" + self.spec["hepmc3"].prefix]

        if self.spec.satisfies("@2.2.0:"):
            args += ["--with-hepmcversion=" + self.spec.variants["hepmc"].value]

        if self.spec.satisfies("@2.0.0:"):
            args += ["--with-fastjet=" + self.spec["fastjet"].prefix]

        if self.spec.satisfies("@2.0.3: +rivet"):
            args += ["--with-rivet=" + self.spec["rivet"].prefix]

        if self.spec.satisfies("@2.1.1:"):
            args += ["--with-boost=" + self.spec["boost"].prefix]

        args += self.enable_or_disable("libs")

        return args
