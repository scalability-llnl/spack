# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sherpa(CMakePackage, AutotoolsPackage):
    """Sherpa is a Monte Carlo event generator for the Simulation of
    High-Energy Reactions of PArticles in lepton-lepton, lepton-photon,
    photon-photon, lepton-hadron and hadron-hadron collisions."""

    homepage = "https://sherpa-team.gitlab.io"
    url = "https://gitlab.com/sherpa-team/sherpa/-/archive/v2.2.11/sherpa-v2.2.11.tar.gz"
    list_url = "https://gitlab.com/sherpa-team/sherpa/-/tags"
    git = "https://gitlab.com/sherpa-team/sherpa.git"

    tags = ["hep", "eic"]

    maintainers("wdconinc", "vvolkl")

    license("GPL-3.0-only")

    version("3.0.0", sha256="e460d8798b323c4ef663293a2c918b1463e9641b35703a54d70d25c852c67d36")
    version("2.2.15", sha256="0300fd719bf6a089b7dc5441f720e669ac1cb030045d87034a4733bee98e7bbc")
    version("2.2.14", sha256="f17d88d7f3bc4234a9db3872e8a3c1f3ef99e1e2dc881ada5ddf848715dc82da")
    version("2.2.13", sha256="ed1fd1372923c191ca44897802d950702b810382260e7464d36ac3234c5c8a64")
    version("2.2.12", sha256="4ba78098e45aaac0bc303d1b5abdc15809f30b407abf9457d99b55e63384c83d")
    version("2.2.11", sha256="5e12761988b41429f1d104f84fdf352775d233cde7a165eb64e14dcc20c3e1bd")

    build_system(
        conditional("cmake", when="@3:"), conditional("autotools", when="@:2"), default="cmake"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    _cxxstd_values = ("11", "14", "17")
    variant(
        "cxxstd",
        default="11",
        values=_cxxstd_values,
        multi=False,
        description="Use the specified C++ standard when building",
    )

    variant("analysis", default=True, description="Enable analysis components")
    variant("mpi", default=False, description="Enable MPI")
    variant("python", default=False, description="Enable Python API")
    variant("hepmc2", default=True, when="@:2", description="Enable HepMC (version 2.x) support")
    variant("hepmc3", default=True, description="Enable HepMC (version 3.x) support")
    variant("hepmc3root", default=False, description="Enable HepMC (version 3.1+) ROOT support")
    variant("rivet", default=False, description="Enable Rivet support")
    variant("fastjet", default=True, when="@:2", description="Enable FASTJET")
    variant("openloops", default=False, description="Enable OpenLoops")
    variant("recola", default=False, description="Enable Recola")
    variant("lhole", default=False, description="Enable Les Houches One-Loop Generator interface")
    variant("root", default=False, description="Enable ROOT support")
    variant("lhapdf", default=True, description="Enable LHAPDF support")
    variant("gzip", default=False, description="Enable gzip support")
    variant("pythia", default=True, description="Enable fragmentation/decay interface to Pythia")
    variant("blackhat", default=False, description="Enable BLACKHAT support")
    variant("ufo", default=False, description="Enable UFO support")
    variant("hztool", default=False, when="@:2", description="Enable HZTOOL support")
    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )
    # cernlib not yet in spack
    # variant('cernlib',    default=False, description='Enable CERNLIB support')

    variant("cms", default=False, description="Append CXXFLAGS used by CMS experiment")

    # Note that the delphes integration seems utterly broken: https://sherpa.hepforge.org/trac/ticket/305

    # autotools dependencies are needed at runtime to compile processes
    depends_on("autoconf", when="@:2")
    depends_on("automake", when="@:2")
    depends_on("libtool", when="@:2")
    depends_on("m4", when="@:2")
    depends_on("texinfo", type="build")
    depends_on("sqlite")

    depends_on("mpi", when="+mpi")
    depends_on("python", when="+python")
    depends_on("swig", when="+python", type="build")
    depends_on("hepmc", when="+hepmc2")
    depends_on("hepmc3", when="+hepmc3")
    depends_on("hepmc3 +rootio", when="+hepmc3root")
    depends_on("rivet", when="+rivet")
    depends_on("fastjet", when="+fastjet")
    depends_on("openloops", when="+openloops")
    # sherpa builds with recola2 with the patch below,
    # but the authors have validated only recola1
    # see https://gitlab.com/sherpa-team/sherpa/-/issues/356
    depends_on("recola@1", when="+recola")
    depends_on("root", when="+root")
    depends_on("lhapdf", when="+lhapdf")
    depends_on("gzip", when="+gzip")
    depends_on("pythia6", when="+pythia @:2")
    depends_on("pythia8", when="+pythia @3:")
    depends_on("blackhat", when="+blackhat")
    depends_on("hztool", when="+hztool")
    # depends_on('cernlib',   when='+cernlib')
    depends_on("libzip", when="@3:")

    filter_compiler_wrappers("share/SHERPA-MC/makelibs")

    for std in _cxxstd_values:
        depends_on("root cxxstd=" + std, when="+root cxxstd=" + std)

    def patch(self):
        filter_file(
            r"#include <sys/sysctl.h>",
            "#ifdef ARCH_DARWIN\n#include <sys/sysctl.h>\n#endif",
            "ATOOLS/Org/Run_Parameter.C",
        )

        if self.spec.satisfies("^recola@2:"):
            filter_file(
                r'#include "recola.h"',
                '#include "recola.hpp"',
                "AddOns/Recola/Recola_Interface.H",
                string=True,
            )

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == "cxxflags":
            flags.append("-std=c++" + self.spec.variants["cxxstd"].value)

            if "+cms" in self.spec:
                flags.extend(["-fuse-cxa-atexit", "-O2"])
                if self.spec.target.family == "x86_64":
                    flags.append("-m64")

        return (None, None, flags)


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        args = [
            self.define_from_variant("SHERPA_ENABLE_ANALYSIS", "analysis"),
            self.define_from_variant("SHERPA_ENABLE_BLACKHAT", "blackhat"),
            self.define_from_variant("SHERPA_ENABLE_GZIP", "gzip"),
            self.define_from_variant("SHERPA_ENABLE_HEPMC3", "hepmc3"),
            self.define_from_variant("SHERPA_ENABLE_HEPMC3_ROOT", "hepmc3root"),
            self.define_from_variant("SHERPA_ENABLE_LHAPDF", "lhapdf"),
            self.define_from_variant("SHERPA_ENABLE_LHOLE", "lhole"),
            self.define_from_variant("SHERPA_ENABLE_MPI", "mpi"),
            self.define_from_variant("SHERPA_ENABLE_OPENLOOPS", "openloops"),
            self.define_from_variant("SHERPA_ENABLE_PYTHIA8", "pythia"),
            self.define_from_variant("SHERPA_ENABLE_PYTHON", "python"),
            self.define_from_variant("SHERPA_ENABLE_RECOLA", "recola"),
            self.define_from_variant("SHERPA_ENABLE_RIVET", "rivet"),
            self.define_from_variant("SHERPA_ENABLE_ROOT", "root"),
            self.define_from_variant("SHERPA_ENABLE_UFO", "ufo"),
        ]
        return args


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    def configure_args(self):
        args = []
        args.append("--enable-binreloc")
        args.append("--enable-hepevtsize=200000")
        args.append("--with-sqlite3=" + self.spec["sqlite"].prefix)
        args.extend(self.enable_or_disable("libs"))
        args.extend(self.enable_or_disable("mpi"))
        args.extend(self.enable_or_disable("pyext", variant="python"))
        args.extend(self.enable_or_disable("analysis"))
        args.extend(self.enable_or_disable("lhole"))
        args.extend(self.enable_or_disable("gzip"))
        args.extend(self.enable_or_disable("pythia"))
        hepmc_root = lambda x: self.spec["hepmc"].prefix
        args.extend(self.enable_or_disable("hepmc2", activation_value=hepmc_root))
        # See https://gitlab.com/sherpa-team/sherpa/-/issues/348
        if self.spec.satisfies("+hepmc3"):
            args.append("--enable-hepmc3=" + self.spec["hepmc3"].prefix)
        if self.spec.satisfies("+rivet"):
            args.append("--enable-rivet=" + self.spec["rivet"].prefix)
        if self.spec.satisfies("+lhapdf"):
            args.append("--enable-lhapdf=" + self.spec["lhapdf"].prefix)

        args.extend(self.enable_or_disable("fastjet", activation_value="prefix"))
        args.extend(self.enable_or_disable("openloops", activation_value="prefix"))
        args.extend(self.enable_or_disable("recola", activation_value="prefix"))
        args.extend(self.enable_or_disable("root", activation_value="prefix"))

        args.extend(self.enable_or_disable("hztool", activation_value="prefix"))
        # args.extend(self.enable_or_disable('cernlib', activation_value='prefix'))
        args.extend(self.enable_or_disable("blackhat", activation_value="prefix"))
        args.extend(self.enable_or_disable("ufo"))

        if self.spec.satisfies("+mpi"):
            args.append("CC=" + self.spec["mpi"].mpicc)
            args.append("MPICXX=" + self.spec["mpi"].mpicxx)
            args.append("CXX=" + self.spec["mpi"].mpicxx)
            args.append("FC=" + self.spec["mpi"].mpifc)

        return args

    def install(self, spec, prefix):
        # Make sure the path to the provided libtool is used instead of the system one
        filter_file(
            r"autoreconf -fi",
            f"autoreconf -fi -I {self.spec['libtool'].prefix.share.aclocal}",
            "AMEGIC++/Main/makelibs",
        )
        make("install")
