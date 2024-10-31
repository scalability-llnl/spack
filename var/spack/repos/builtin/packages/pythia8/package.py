# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pythia8(AutotoolsPackage):
    """The Pythia program is a standard tool for the generation of events in
    high-energy collisions, comprising a coherent set of physics models for
    the evolution from a few-body hard process to a complex multiparticle
    final state."""

    homepage = "http://home.thep.lu.se/Pythia/"
    url = "https://pythia.org/download/pythia83/pythia8306.tgz"
    list_url = "https://pythia.org/releases/"

    tags = ["hep"]

    maintainers("ChristianTackeGSI")

    license("GPL-2.0-only")

    version("8.311", sha256="2782d5e429c1543c67375afe547fd4c4ca0720309deb008f7db78626dc7d1464")
    version("8.310", sha256="90c811abe7a3d2ffdbf9b4aeab51cf6e0a5a8befb4e3efa806f3d5b9c311e227")
    version("8.309", sha256="5bdafd9f2c4a1c47fd8a4e82fb9f0d8fcfba4de1003b8e14be4e0347436d6c33")
    version("8.308", sha256="c2e8c8d38136d85fc0bc9c9fad4c2db679b0819b7d2b6fc9a47f80f99538b4e3")
    version("8.307", sha256="e5b14d44aa5943332e32dd5dda9a18fdd1a0085c7198e28d840e04167fa6013d")
    version("8.306", sha256="734803b722b1c1b53c8cf2f0d3c30747c80fc2dde5e0ba141bc9397dad37a8f6")
    version("8.304", sha256="d3897018fb6d545eaf93bf43f32580c984a9bff49259d9dd29dff6edfbe9d9a1")
    version("8.303", sha256="cd7c2b102670dae74aa37053657b4f068396988ef7da58fd3c318c84dc37913e")
    version("8.302", sha256="7372e4cc6f48a074e6b7bc426b040f218ec4a64b0a55e89da6af56933b5f5085")
    version("8.301", sha256="51382768eb9aafb97870dca1909516422297b64ef6a6b94659259b3e4afa7f06")
    version(
        "8.244",
        sha256="e34880f999daf19cdd893a187123927ba77d1bf851e30f6ea9ec89591f4c92ca",
        deprecated=True,
    )
    version(
        "8.240",
        sha256="d27495d8ca7707d846f8c026ab695123c7c78c7860f04e2c002e483080418d8d",
        deprecated=True,
    )
    version(
        "8.235",
        sha256="e82f0d6165a8250a92e6aa62fb53201044d8d853add2fdad6d3719b28f7e8e9d",
        deprecated=True,
    )
    version(
        "8.230",
        sha256="332fad0ed4f12e6e0cb5755df0ae175329bc16bfaa2ae472d00994ecc99cd78d",
        deprecated=True,
    )
    version(
        "8.212",
        sha256="f8fb4341c7e8a8be3347eb26b00329a388ccf925313cfbdba655a08d7fd5a70e",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated

    variant(
        "cxxstd",
        default="11",
        values=("11", "17", "20", "23"),
        multi=False,
        description="Use the specified C++ standard when building",
    )

    variant("shared", default=True, description="Build shared library")
    variant("gzip", default=False, description="Build with gzip support, for reading lhe.gz files")
    variant(
        "hepmc", default=True, description="Export PYTHIA events to the HEPMC format, version 2"
    )
    variant(
        "hepmc3", default=True, description="Export PYTHIA events to the HEPMC format, version 3"
    )
    variant("evtgen", default=False, description="Particle decays with the EvtGen decay package")
    variant("root", default=False, description="Use ROOT trees and histograms with PYTHIA")
    variant(
        "fastjet",
        default=False,
        description="Building of jets using the FastJet package, version 3",
    )
    variant("lhapdf", default=False, description="Support the use of external PDF sets via LHAPDF")
    variant("rivet", default=False, description="Support use of RIVET through direct interface")
    variant("python", default=False, description="Interface to use PYTHIA in Python")
    variant(
        "madgraph5amc",
        default=False,
        description="MadGraph matrix element plugins for parton showers",
    )
    variant("openmpi", default=False, description="Multi-threading support via OpenMP")
    variant("mpich", default=False, description="Multi-threading support via MPICH")
    variant("hdf5", default=False, description="Support the use of HDF5 format")

    depends_on("zlib-api", when="+gzip")
    depends_on("rsync", type="build")
    depends_on("hepmc", when="+hepmc")
    depends_on("hepmc3", when="+hepmc3")
    depends_on("root", when="+root")
    depends_on("evtgen", when="+evtgen")
    depends_on("fastjet@3.0.0:", when="+fastjet")
    depends_on("lhapdf@6.2:", when="+lhapdf")
    depends_on("boost", when="+lhapdf @:8.213")
    depends_on("rivet", when="+rivet")
    depends_on("python", when="+python")
    depends_on("madgraph5amc", when="+madgraph5amc")
    depends_on("openmpi", when="+openmpi")
    depends_on("mpich", when="+mpich")
    depends_on("hdf5", when="+hdf5")
    depends_on("highfive@2.2", when="+hdf5")

    extends("python", when="+python")

    conflicts(
        "^evtgen+pythia8",
        when="+evtgen",
        msg="Building pythia with evtgen bindings and "
        "evtgen with pythia bindings results in a circular dependency "
        "that cannot be resolved at the moment! "
        "Use pythia8+evtgen^evtgen~pythia8",
    )

    conflicts("+evtgen", when="~hepmc", msg="+evtgen requires +hepmc")
    conflicts("+mpich", when="@:8.304", msg="MPICH support was added in 8.304")
    conflicts("+hdf5", when="@:8.304", msg="HDF5 support was added in 8.304")
    conflicts("+hdf5", when="~mpich", msg="MPICH is required for reading HDF5 files")

    filter_compiler_wrappers("Makefile.inc", relative_root="share/Pythia8/examples")

    @run_before("configure")
    def setup_cxxstd(self):
        filter_file(
            r"-std=c\+\+[0-9][0-9]", f"-std=c++{self.spec.variants['cxxstd'].value}", "configure"
        )

    # Fix for https://gitlab.com/Pythia8/releases/-/issues/428
    @when("@:8.311")
    def patch(self):
        filter_file(
            r"[/]examples[/]Makefile[.]inc\|;n' \\", "/examples/Makefile.inc|' \\", "configure"
        )

    def configure_args(self):
        args = []

        if self.spec.satisfies("@:8.301 +shared"):
            # Removed in 8.301
            args.append("--enable-shared")

        if "+hepmc" in self.spec:
            args.append("--with-hepmc2=%s" % self.spec["hepmc"].prefix)
        else:
            args.append("--without-hepmc2")

        if "+lhapdf" in self.spec:
            args.append("--with-lhapdf6=%s" % self.spec["lhapdf"].prefix)
            if self.spec.satisfies("@:8.213"):
                args.append("--with-lhapdf6-plugin=LHAPDF6.h")
                args.append("--with-boost=" + self.spec["boost"].prefix)

        if "+madgraph5amc" in self.spec:
            args.append("--with-mg5mes=" + self.spec["madgraph5amc"].prefix)

        args += self.with_or_without("hepmc3", activation_value="prefix")

        if "+fastjet" in self.spec:
            args.append("--with-fastjet3=" + self.spec["fastjet"].prefix)

        args += self.with_or_without("evtgen", activation_value="prefix")
        args += self.with_or_without("root", activation_value="prefix")
        args += self.with_or_without("rivet", activation_value="prefix")
        if self.spec.satisfies("+rivet"):
            args.append("--with-yoda=" + self.spec["yoda"].prefix)

        args += self.with_or_without("python", activation_value="prefix")
        args += self.with_or_without("openmp", activation_value="prefix", variant="openmpi")
        args += self.with_or_without("mpich", activation_value="prefix")
        args += self.with_or_without("hdf5", activation_value="prefix")

        if self.spec.satisfies("+hdf5"):
            args.append("--with-highfive=" + self.spec["highfive"].prefix)

        args += self.with_or_without(
            "gzip", activation_value=lambda x: self.spec["zlib-api"].prefix
        )

        return args

    def url_for_version(self, version):
        url = self.url.rsplit("/", 2)[0]
        dirname = "pythia" + str(version.joined)[:2]
        fname = "pythia" + str(version.joined) + ".tgz"

        return url + "/" + dirname + "/" + fname

    def setup_common_env(self, env):
        env.set("PYTHIA8", self.prefix)
        env.set("PYTHIA8DATA", self.prefix.share.Pythia8.xmldoc)

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_common_env(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_common_env(env)
