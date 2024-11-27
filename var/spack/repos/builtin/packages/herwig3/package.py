# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Herwig3(AutotoolsPackage):
    """Herwig is a multi-purpose particle physics event generator."""

    homepage = "https://herwig.hepforge.org"
    url = "https://herwig.hepforge.org/downloads/Herwig-7.2.1.tar.bz2"

    tags = ["hep"]

    license("GPL-3.0-only")

    version("7.2.3", sha256="5599899379b01b09e331a2426d78d39b7f6ec126db2543e9d340aefe6aa50f84")
    version("7.2.2", sha256="53e06b386df5bc20fe268b6c8ba50f1e62b6744e577d383ec836ea3fc672c383")
    version("7.2.1", sha256="d4fff32f21c5c08a4b2e563c476b079859c2c8e3b78d853a8a60da96d5eea686")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("lhapdf")
    depends_on("lhapdfsets", type="build")
    depends_on("thepeg@2.2.1", when="@7.2.1")
    depends_on("thepeg@2.2.2", when="@7.2.2")
    depends_on("thepeg@2.2.3", when="@7.2.3")
    depends_on("evtgen")

    depends_on("boost +math+test")
    depends_on("python", type=("build", "run"))
    depends_on("gsl")
    depends_on("fastjet")
    depends_on("vbfnlo@3:", when="+vbfnlo")
    depends_on("madgraph5amc")
    depends_on("njet", when="+njet")
    depends_on("py-gosam")
    depends_on("njet")
    depends_on("gosam-contrib")

    # OpenLoops fail to build on PPC64: error: detected recursion whilst expanding macro "vector"
    depends_on("openloops", when="target=aarch64:")
    depends_on("openloops", when="target=x86_64:")

    force_autoreconf = True

    variant("vbfnlo", default=True, description="Use VBFNLO")
    variant("njet", default=True, description="Use NJet")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = [
            "--with-gsl=" + self.spec["gsl"].prefix,
            "--with-thepeg=" + self.spec["thepeg"].prefix,
            "--with-thepeg-headers=" + self.spec["thepeg"].prefix.include,
            "--with-fastjet=" + self.spec["fastjet"].prefix,
            "--with-boost=" + self.spec["boost"].prefix,
            "--with-madgraph=" + self.spec["madgraph5amc"].prefix,
            "--with-openloops=" + self.spec["openloops"].prefix,
            "--with-gosam-contrib=" + self.spec["gosam-contrib"].prefix,
            "--with-evtgen=" + self.spec["evtgen"].prefix,
            "--with-gosam=" + self.spec["py-gosam"].prefix,
        ]

        if self.spec.satisfies("+njet"):
            args.append("--with-njet=" + self.spec["njet"].prefix)

        if self.spec.satisfies("+vbfnlo"):
            args.append("--with-vbfnlo=" + self.spec["vbfnlo"].prefix)

        return args

    def flag_handler(self, name, flags):
        if name == "fflags":
            flags.append("-std=legacy")
            return (flags, None, None)
        return (flags, None, None)

    def setup_build_environment(self, env):
        thepeg_home = self.spec["thepeg"].prefix
        env.prepend_path("LD_LIBRARY_PATH", thepeg_home.lib.ThePEG)
        env.set("HERWIGINCLUDE", "-I" + self.prefix.include)
        env.set("BOOSTINCLUDE", "-I" + self.spec["boost"].prefix.include)
        env.set("HERWIGINSTALL", self.prefix)

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make("install")
